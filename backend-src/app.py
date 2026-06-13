import os
import time
import logging

import mysql.connector
from mysql.connector import Error as MySQLError

from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv


# ══════════════════════════════════════════════════════════════════
# ENVIRONMENT & LOGGING
# ══════════════════════════════════════════════════════════════════

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# FLASK APPLICATION
# ══════════════════════════════════════════════════════════════════

app = Flask(__name__)
metrics = PrometheusMetrics(app)
from prometheus_client import Counter, Gauge

user_registrations_total = Counter(
    "user_registrations_total",
    "Total number of user registrations"
)

user_logins_total = Counter(
    "user_logins_total",
    "Total number of successful logins"
)

task_operations_total = Counter(
    "task_operations_total",
    "Total task operations",
    ["operation"]
)

db_connection_status = Gauge(
    "db_connection_status",
    "Database connection status"
)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600   # 1 hour

jwt = JWTManager(app)


# ══════════════════════════════════════════════════════════════════
# DATABASE CONNECTION  (retry until MySQL is ready)
# ══════════════════════════════════════════════════════════════════

def get_connection():
    """Return a fresh MySQL connection."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "devopsdb"),
        connection_timeout=10,
    )


def wait_for_db(retries: int = 15, delay: int = 5):
    """Block startup until MySQL accepts connections."""
    for attempt in range(1, retries + 1):
        try:
            conn = get_connection()
            log.info("MySQL connection established.")
            return conn
        except MySQLError as err:
            log.warning("MySQL not ready (attempt %d/%d): %s", attempt, retries, err)
            time.sleep(delay)
    raise RuntimeError("Could not connect to MySQL after multiple retries.")


connection = wait_for_db()


# ══════════════════════════════════════════════════════════════════
# SCHEMA INITIALISATION
# ══════════════════════════════════════════════════════════════════

def init_schema():
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80)  NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                title      VARCHAR(200) NOT NULL,
                status     ENUM('Pending','In Progress','Completed') DEFAULT 'Pending',
                user_id    INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                           ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        connection.commit()
        log.info("Database schema verified.")
    finally:
        cursor.close()


init_schema()


# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════

def ok(data=None, message=None, status=200):
    body = {"success": True}
    if message:
        body["message"] = message
    if data is not None:
        body["data"] = data
    return jsonify(body), status


def fail(message, status=400):
    return jsonify({"success": False, "message": message}), status


def ensure_connection():
    """Reconnect if the MySQL connection has dropped."""
    global connection
    try:
        connection.ping(reconnect=True, attempts=3, delay=2)
    except MySQLError:
        log.warning("Lost DB connection — reconnecting.")
        connection = get_connection()


def validate_json(*required_fields):
    """Return (data, error_response) tuple."""
    data = request.get_json(silent=True)
    if data is None:
        return None, fail("Request body must be valid JSON.")
    for field in required_fields:
        if not data.get(field, "").strip():
            return None, fail(f"'{field}' is required.")
    return data, None


# ══════════════════════════════════════════════════════════════════
# JWT ERROR HANDLERS
# ══════════════════════════════════════════════════════════════════

@jwt.unauthorized_loader
def missing_token(_err):
    return fail("Authentication token is missing.", 401)


@jwt.invalid_token_loader
def invalid_token(_err):
    return fail("Authentication token is invalid.", 401)


@jwt.expired_token_loader
def expired_token(_jwt_header, _jwt_data):
    return fail("Authentication token has expired. Please log in again.", 401)


# ══════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════════════════════════════

@app.route("/health", methods=["GET"])
def health():
    try:
        ensure_connection()
        cur = connection.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        db_status = "connected"
        db_connection_status.set(1)
    except MySQLError:
        db_status = "unavailable"
        db_connection_status.set(0)
    return ok({"api": "running", "database": db_status})


# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════

@app.route("/", methods=["GET"])
def home():
    return ok(message="DevOps Task Platform API v3 is running.")


# ══════════════════════════════════════════════════════════════════
# AUTH — REGISTER
# ══════════════════════════════════════════════════════════════════

@app.route("/api/register", methods=["POST"])
def register():
    data, err = validate_json("username", "password")
    if err:
        return err

    username = data["username"].strip()
    password = data["password"].strip()

    if len(username) < 3:
        return fail("Username must be at least 3 characters.")
    if len(username) > 80:
        return fail("Username must be 80 characters or fewer.")
    if len(password) < 6:
        return fail("Password must be at least 6 characters.")

    hashed = generate_password_hash(password)
    ensure_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed),
        )
        connection.commit()
        user_registrations_total.inc()
        log.info("New user registered: %s", username)
        return ok(message="Account created successfully.")
    except MySQLError as err:
        if "Duplicate entry" in str(err):
            return fail("Username already exists. Please choose another.", 409)
        log.error("Register error: %s", err)
        return fail("Registration failed. Please try again.", 500)
    finally:
        cursor.close()


# ══════════════════════════════════════════════════════════════════
# AUTH — LOGIN
# ══════════════════════════════════════════════════════════════════

@app.route("/api/login", methods=["POST"])
def login():
    data, err = validate_json("username", "password")
    if err:
        return err

    username = data["username"].strip()
    password = data["password"].strip()

    ensure_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
    finally:
        cursor.close()

    if not user or not check_password_hash(user["password"], password):
        return fail("Invalid username or password.", 401)

    token = create_access_token(identity=str(user["id"]))
    log.info("User logged in: %s", username)
    user_logins_total.inc()
    return ok(
        data={"token": token, "username": username},
        message="Login successful.",
    )


# ══════════════════════════════════════════════════════════════════
# TASKS — GET ALL
# ══════════════════════════════════════════════════════════════════

@app.route("/api/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    ensure_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, title, status, created_at, updated_at "
            "FROM tasks WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,),
        )
        tasks = cursor.fetchall()
        # Serialise datetime objects
        for task in tasks:
            for key in ("created_at", "updated_at"):
                if task.get(key):
                    task[key] = task[key].strftime("%Y-%m-%d %H:%M")
    finally:
        cursor.close()
    return ok(data=tasks)


# ══════════════════════════════════════════════════════════════════
# TASKS — ADD
# ══════════════════════════════════════════════════════════════════

@app.route("/api/tasks", methods=["POST"])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data, err = validate_json("title")
    if err:
        return err

    title = data["title"].strip()
    if len(title) > 200:
        return fail("Task title must be 200 characters or fewer.")

    ensure_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (title, status, user_id) VALUES (%s, 'Pending', %s)",
            (title, user_id),
        )
        connection.commit()
        task_operations_total.labels(
           operation="create"
        ).inc()
        task_id = cursor.lastrowid
    finally:
        cursor.close()

    log.info("Task %d added by user %s", task_id, user_id)
    return ok(data={"id": task_id}, message="Task added successfully.", status=201)


# ══════════════════════════════════════════════════════════════════
# TASKS — UPDATE
# ══════════════════════════════════════════════════════════════════

VALID_STATUSES = {"Pending", "In Progress", "Completed"}

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data, err = validate_json("title", "status")
    if err:
        return err

    title  = data["title"].strip()
    status = data["status"].strip()

    if status not in VALID_STATUSES:
        return fail(f"Status must be one of: {', '.join(VALID_STATUSES)}.")
    if len(title) > 200:
        return fail("Task title must be 200 characters or fewer.")

    ensure_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE tasks SET title = %s, status = %s "
            "WHERE id = %s AND user_id = %s",
            (title, status, task_id, user_id),
        )
        connection.commit()

        if cursor.rowcount == 0:
          return fail("Task not found or access denied.", 404)

        task_operations_total.labels(
          operation="update"
        ).inc()
    finally:
        cursor.close()

    return ok(message="Task updated successfully.")


# ══════════════════════════════════════════════════════════════════
# TASKS — DELETE
# ══════════════════════════════════════════════════════════════════

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    ensure_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s AND user_id = %s",
            (task_id, user_id),
        )
        connection.commit()

        if cursor.rowcount == 0:
            return fail("Task not found or access denied.", 404)

        task_operations_total.labels(
            operation="delete"
        ).inc()

    finally:
        cursor.close()

    log.info("Task %d deleted by user %s", task_id, user_id)
    return ok(message="Task deleted successfully.")


# ══════════════════════════════════════════════════════════════════
# GLOBAL ERROR HANDLERS
# ══════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(_e):
    return fail("The requested endpoint does not exist.", 404)


@app.errorhandler(405)
def method_not_allowed(_e):
    return fail("HTTP method not allowed for this endpoint.", 405)


@app.errorhandler(500)
def internal_error(e):
    log.error("Unhandled server error: %s", e)
    return fail("An unexpected server error occurred.", 500)


# ══════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
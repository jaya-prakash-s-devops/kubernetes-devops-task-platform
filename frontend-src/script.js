"use strict";

// ═══════════════════════════════════════════════
// CONFIG
// ═══════════════════════════════════════════════

const API = "http://192.168.1.64:30500/api";

// ═══════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════

let token       = localStorage.getItem("token")    || "";
let currentUser = localStorage.getItem("username") || "";
let tasks       = [];
let editingId   = null;
let activeFilter = "All";

// ═══════════════════════════════════════════════
// INITIALISE
// ═══════════════════════════════════════════════

document.addEventListener("DOMContentLoaded", () => {
  if (token) {
    showDashboard();
    fetchTasks();
  } else {
    showAuth();
  }
});

// ═══════════════════════════════════════════════
// SCREEN SWITCHING
// ═══════════════════════════════════════════════

function showAuth() {
  show("auth-screen");
  hide("dashboard-screen");
}

function showDashboard() {
  hide("auth-screen");
  show("dashboard-screen");
  document.getElementById("nav-username").textContent = currentUser;
}

function switchTab(tab) {
  const isLogin = tab === "login";
  toggle("login-form",    isLogin);
  toggle("register-form", !isLogin);
  document.getElementById("tab-login").classList.toggle("active",    isLogin);
  document.getElementById("tab-register").classList.toggle("active", !isLogin);
  clearNotification("auth-notification");
}

// ═══════════════════════════════════════════════
// AUTH — LOGIN
// ═══════════════════════════════════════════════

async function handleLogin(e) {
  e.preventDefault();
  const username = val("login-username");
  const password = val("login-password");

  setLoading("login-btn", true);
  clearNotification("auth-notification");

  const { ok, data, message } = await api("POST", "/login", { username, password });

  setLoading("login-btn", false);

  if (ok) {
    token       = data.data.token;
    currentUser = data.data.username;
    localStorage.setItem("token",    token);
    localStorage.setItem("username", currentUser);
    showDashboard();
    fetchTasks();
  } else {
    notify("auth-notification", message, "error");
  }
}

// ═══════════════════════════════════════════════
// AUTH — REGISTER
// ═══════════════════════════════════════════════

async function handleRegister(e) {
  e.preventDefault();
  const username = val("reg-username");
  const password = val("reg-password");

  setLoading("register-btn", true);
  clearNotification("auth-notification");

  const { ok, data, message } = await api("POST", "/register", { username, password });

  setLoading("register-btn", false);

  if (ok) {
    notify("auth-notification", "Account created! You can now log in.", "success");
    document.getElementById("register-form").reset();
    setTimeout(() => switchTab("login"), 1200);
  } else {
    notify("auth-notification", message, "error");
  }
}

// ═══════════════════════════════════════════════
// AUTH — LOGOUT
// ═══════════════════════════════════════════════

function logout() {
  token       = "";
  currentUser = "";
  tasks       = [];
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  showAuth();
  switchTab("login");
}

// ═══════════════════════════════════════════════
// TASKS — FETCH
// ═══════════════════════════════════════════════

async function fetchTasks() {
  renderSkeletons();

  const { ok, data, message } = await api("GET", "/tasks");

  if (ok) {
    tasks = data.data || [];
    renderTasks();
    updateStats();
  } else if (message.includes("expired") || message.includes("invalid")) {
    logout();
  } else {
    notify("task-notification", "Failed to load tasks: " + message, "error");
    renderTasks();
  }
}

// ═══════════════════════════════════════════════
// TASKS — ADD
// ═══════════════════════════════════════════════

async function handleAddTask(e) {
  e.preventDefault();
  const title = val("task-input");
  if (!title) return;

  setLoading("add-task-btn", true);
  clearNotification("task-notification");

  const { ok, message } = await api("POST", "/tasks", { title });

  setLoading("add-task-btn", false);

  if (ok) {
    document.getElementById("task-input").value = "";
    notify("task-notification", "Task added successfully.", "success");
    await fetchTasks();
  } else {
    notify("task-notification", message, "error");
  }
}

// ═══════════════════════════════════════════════
// TASKS — DELETE
// ═══════════════════════════════════════════════

async function deleteTask(id) {
  const { ok, message } = await api("DELETE", `/tasks/${id}`);
  if (ok) {
    tasks = tasks.filter(t => t.id !== id);
    renderTasks();
    updateStats();
  } else {
    notify("task-notification", message, "error");
  }
}

// ═══════════════════════════════════════════════
// TASKS — EDIT MODAL
// ═══════════════════════════════════════════════

function openEditModal(task) {
  editingId = task.id;
  document.getElementById("edit-title").value  = task.title;
  document.getElementById("edit-status").value = task.status;
  show("edit-modal");
}

function closeEditModal() {
  editingId = null;
  hide("edit-modal");
}

function closeModal(e) {
  if (e.target.id === "edit-modal") closeEditModal();
}

// ═══════════════════════════════════════════════
// TASKS — UPDATE
// ═══════════════════════════════════════════════

async function handleUpdateTask(e) {
  e.preventDefault();
  const title  = document.getElementById("edit-title").value.trim();
  const status = document.getElementById("edit-status").value;

  const { ok, message } = await api("PUT", `/tasks/${editingId}`, { title, status });

  if (ok) {
    closeEditModal();
    notify("task-notification", "Task updated successfully.", "success");
    await fetchTasks();
  } else {
    notify("task-notification", message, "error");
  }
}

// ═══════════════════════════════════════════════
// FILTER
// ═══════════════════════════════════════════════

function setFilter(btn) {
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  activeFilter = btn.dataset.filter;
  renderTasks();
}

// ═══════════════════════════════════════════════
// RENDER
// ═══════════════════════════════════════════════

function renderTasks() {
  const list = document.getElementById("task-list");

  const filtered = activeFilter === "All"
    ? tasks
    : tasks.filter(t => t.status === activeFilter);

  if (filtered.length === 0) {
    list.innerHTML = `
      <div class="task-empty" id="task-empty">
        <div class="empty-icon">📋</div>
        <p>${activeFilter === "All" ? "No tasks yet. Add your first task above." : `No "${activeFilter}" tasks.`}</p>
      </div>`;
    return;
  }

  list.innerHTML = filtered.map(task => {
    const badgeClass = task.status.replace(" ", "-");
    const dot = task.status === "Completed" ? "✓" : task.status === "In Progress" ? "◉" : "○";
    return `
      <div class="task-card ${task.status === "Completed" ? "completed" : ""}">
        <div class="task-left">
          <div class="task-title">${escHtml(task.title)}</div>
          <div class="task-meta">Added ${task.created_at || "recently"}</div>
        </div>
        <div class="task-right">
          <span class="status-badge ${badgeClass}">${dot} ${task.status}</span>
          <button class="btn btn-outline btn-icon" title="Edit" onclick='openEditModal(${JSON.stringify(task)})'>✎</button>
          <button class="btn btn-danger   btn-icon" title="Delete" onclick="deleteTask(${task.id})">✕</button>
        </div>
      </div>`;
  }).join("");
}

function renderSkeletons() {
  const list = document.getElementById("task-list");
  list.innerHTML = [1, 2, 3].map(() => `<div class="skeleton"></div>`).join("");
}

function updateStats() {
  const total    = tasks.length;
  const pending  = tasks.filter(t => t.status === "Pending").length;
  const progress = tasks.filter(t => t.status === "In Progress").length;
  const done     = tasks.filter(t => t.status === "Completed").length;

  document.getElementById("stat-total").textContent    = total;
  document.getElementById("stat-pending").textContent  = pending;
  document.getElementById("stat-progress").textContent = progress;
  document.getElementById("stat-done").textContent     = done;
}

// ═══════════════════════════════════════════════
// API WRAPPER
// ═══════════════════════════════════════════════

async function api(method, path, body = null) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  try {
    const res = await fetch(`${API}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    });

    const data = await res.json();

    if (res.ok) {
      return { ok: true, data, message: data.message || "" };
    }
    return { ok: false, data, message: data.message || "An error occurred." };

  } catch (err) {
    console.error("API error:", err);
    return { ok: false, data: null, message: "Network error. Please check your connection." };
  }
}

// ═══════════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════════

function show(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.remove("hidden");
    }
}

function hide(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.add("hidden");
    }
}

function toggle(id, visible) {
    visible ? show(id) : hide(id);
}

function val(id) {
    const el = document.getElementById(id);
    return el ? el.value.trim() : "";
}

function setLoading(btnId, loading) {
  const btn = document.getElementById(btnId);

  if (!btn) return;

  const text = btn.querySelector(".btn-text");
  const spinner = btn.querySelector(".btn-spinner");

  btn.disabled = loading;

  if (text) {
    text.classList.toggle("hidden", loading);
  }

  if (spinner) {
    spinner.classList.toggle("hidden", !loading);
  }
}

function notify(targetId, message, type) {
  const el = document.getElementById(targetId);
  el.textContent  = message;
  el.className    = `notification ${type}`;
  el.classList.remove("hidden");
  clearTimeout(el._timer);
  el._timer = setTimeout(() => el.classList.add("hidden"), 4000);
}

function clearNotification(targetId) {
  const el = document.getElementById(targetId);
  el.classList.add("hidden");
  el.textContent = "";
}

function escHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
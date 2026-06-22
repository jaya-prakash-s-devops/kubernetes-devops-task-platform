
<div align="center">

# ⚙️ DevOps Task Platform

*A full-stack task management application deployed on a self-managed K3s Kubernetes cluster,*
*built to demonstrate real-world GitOps, CI/CD, containerization, and production-grade observability.*

<br>

![Platform](https://img.shields.io/badge/Kubernetes-K3s-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitOps](https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Docker](https://img.shields.io/badge/Containers-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

![Flask](https://img.shields.io/badge/Backend-Python%20Flask-000000?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![DockerHub](https://img.shields.io/badge/Registry-Docker%20Hub-2496ED?style=flat-square&logo=docker&logoColor=white)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Application Features](#-application-features)
- [GitOps Workflow](#-gitops-workflow)
- [Kubernetes Infrastructure](#-kubernetes-infrastructure)
- [CI Pipeline](#-ci-pipeline)
- [Monitoring and Observability](#-monitoring-and-observability)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Screenshots](#-screenshots)
- [Author](#-author)

---

## 🔍 Overview

The **DevOps Task Platform** is a portfolio project that simulates a production engineering environment from the ground up. It wraps a simple full-stack task management application inside a complete DevOps lifecycle:

- **Docker** containerizes each service for consistent, portable builds
- **K3s Kubernetes** orchestrates workloads with replica management, health probes, and rolling updates
- **GitHub Actions** automates the CI pipeline — building images, pushing to Docker Hub, and updating manifests on every commit
- **ArgoCD** watches the Git repository and continuously reconciles the cluster to the declared state, enabling self-healing and GitOps-native deployments
- **Prometheus and Grafana** provide full observability across the node, application, and database layers with custom dashboards and alerting

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Developer Pushes Code                        │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions CI Pipeline                     │
│                                                                       │
│   Build Frontend Image ──┐                                            │
│   Build Backend Image  ──┼──▶  Push to Docker Hub                    │
│                           │                                            │
│                           └──▶  Update image tags in K8s manifests   │
│                                 Commit manifests back to Git          │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          ArgoCD (GitOps)                              │
│                                                                       │
│   Watches Git repo ──▶ Detects diff ──▶ Auto-syncs K3s cluster       │
│   Continuous reconciliation + Self-healing                            │
└─────────────────────────────────┬────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        K3s Kubernetes Cluster                         │
│                                                                       │
│   Namespace: devops-platform          Namespace: monitoring           │
│   ┌─────────────────────────────┐    ┌──────────────────────────┐    │
│   │  Frontend   (3 replicas)    │    │  Prometheus              │    │
│   │  Backend    (3 replicas)    │    │  Grafana                 │    │
│   │  MySQL      (1 replica)     │    │  Alertmanager            │    │
│   │  ConfigMaps + Secrets       │    │  Node Exporter           │    │
│   │  PVC for MySQL              │    │  MySQL Exporter          │    │
│   └─────────────────────────────┘    │  ServiceMonitors         │    │
│                                      └──────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python, Flask |
| **Database** | MySQL |
| **Containerization** | Docker, Docker Hub |
| **Orchestration** | K3s Kubernetes |
| **GitOps** | ArgoCD |
| **CI Pipeline** | GitHub Actions |
| **Monitoring** | Prometheus, Grafana, Node Exporter, MySQL Exporter |
| **Alerting** | Alertmanager |
| **Source Control** | Git, GitHub |

---

## ✅ Application Features

The application is a task manager with full CRUD capability:

- **User Registration** — Create a new account
- **User Login / Logout** — Session-based authentication
- **Task Creation** — Add tasks with a description
- **Task Management** — View, update, and delete tasks
- **Status Tracking** — Mark tasks as `Pending`, `In Progress`, or `Completed`
- **Filtered Views** — Filter the task list by status

---

## 🔄 GitOps Workflow

```
1.  Developer pushes code to GitHub
          │
          ▼
2.  GitHub Actions triggers automatically
    ├── Builds frontend Docker image
    ├── Builds backend Docker image
    ├── Tags images with Git commit SHA
    └── Pushes both images to Docker Hub
          │
          ▼
3.  GitHub Actions updates Kubernetes manifests
    └── Commits new image tags back to the repository
          │
          ▼
4.  ArgoCD detects the manifest change
    ├── Compares desired state (Git) vs actual state (cluster)
    ├── Automatically syncs the difference
    └── Self-heals any drift without manual intervention
          │
          ▼
5.  K3s cluster runs the updated application
```

Every deployment is tagged with the Git commit SHA, making every release fully auditable and rollback-ready.

---

## ☸️ Kubernetes Infrastructure

### Namespaces

| Namespace | Purpose |
|---|---|
| `devops-platform` | Application workloads |
| `monitoring` | Observability stack |

### Workloads

| Kind | Name | Replicas |
|---|---|---|
| Deployment | `backend` | 3 |
| Deployment | `frontend` | 3 |
| Deployment | `mysql` | 1 |

### Services

| Service | Type | Port(s) |
|---|---|---|
| `frontend-service` | NodePort | 80 → 30080 |
| `backend-service` | NodePort | 5000 → 30500 |
| `mysql` | ClusterIP | 3306, 9104 |

### Kubernetes Features Implemented

- **Namespace isolation** — Application and monitoring are fully separated
- **ConfigMaps** — Non-sensitive configuration externalized from containers
- **Secrets** — Database credentials stored as Kubernetes Secrets
- **Persistent Volume Claim** — MySQL data survives pod restarts
- **Readiness Probes** — Traffic only routed to pods that pass health checks
- **Liveness Probes** — Unhealthy pods are automatically restarted
- **Rolling Updates** — Deployments update with zero downtime via ArgoCD sync

---

## ⚙️ CI Pipeline

The GitHub Actions pipeline runs automatically on every push to `main`:

```
Trigger: push to main
    │
    ├── Step 1 ── Build frontend Docker image
    ├── Step 2 ── Build backend Docker image
    ├── Step 3 ── Push images to Docker Hub (tagged with commit SHA)
    └── Step 4 ── Patch image tags in Kubernetes manifests
                  └── Commit updated manifests back to GitHub
                        └── ArgoCD detects change and syncs cluster
```

**GitHub Actions secrets required:**

| Secret | Purpose |
|---|---|
| `DOCKER_USERNAME` | Docker Hub login |
| `DOCKER_PASSWORD` | Docker Hub password or access token |

---

## 📊 Monitoring and Observability

### Prometheus Scrape Targets

| Target | Exporter | Metrics |
|---|---|---|
| Backend pods | Built-in `/metrics` | Request rate, response time, error rate, success % |
| MySQL | MySQL Exporter (9104) | Queries/sec, connections, uptime |
| Node | Node Exporter (9100) | CPU %, memory %, disk I/O |
| Kubernetes | kube-state-metrics | Pod count, deployment health |
| Prometheus | Self-scrape | Prometheus internals |

All targets are configured using **Prometheus ServiceMonitors** for automatic discovery.

### Grafana Dashboards

**Infrastructure Health**
- Node Memory Usage %
- Node CPU Usage %
- Backend Pods Up / Available

**Application Metrics**
- Total HTTP Requests — `2,590+`
- Backend Request Rate per pod
- Backend Response Time
- Backend Success Rate — `100%`
- Backend Error Rate — `0`

**Cluster and Database Health**
- Total Pods — `22` / Running — `22`
- Cluster Health — `1`
- MySQL Database Up — `1`
- Database Connectivity — `1`

**Database Performance**
- MySQL Queries/sec
- MySQL Active Connections — `7`
- MySQL Uptime — `17,906 seconds`
- Database Error Rate

### Monitoring Access

| Service | URL |
|---|---|
| Grafana | `http://<NODE-IP>:32000` |
| Prometheus | `http://<NODE-IP>:30090` |
| ArgoCD | `http://<NODE-IP>:8080` |

---

## 📁 Project Structure

```
kubernetes-devops-task-platform/
├── .github/
│   └── workflows/
│       ├── deploy.yml                   # Full CI/CD pipeline
│       └── deploy-ci-only.yml           # CI-only workflow
│
├── argocd/
│   └── application.yml                  # ArgoCD Application manifest
│
├── backend/                             # Backend Kubernetes manifests
├── backend-src/                         # Python Flask source code
│
├── frontend/                            # Frontend Kubernetes manifests
├── frontend-src/                        # HTML / CSS / JS source code
│
├── k8/                                  # Core Kubernetes manifests
├── mysql/                               # MySQL deployment manifests
│
├── monitoring/
│   ├── alertmanager/
│   │   ├── alertmanager-config.yml
│   │   └── alertmanager-secret.yml
│   ├── alerts/
│   │   ├── backend-alerts.yml
│   │   ├── mysql-alerts.yml
│   │   └── test-alert.yml
│   ├── backend-service-monitor.yml
│   ├── mysql-service-monitor.yml
│   └── values.yml
│
└── docs/
    └── screenshots/
```

---

## 🚀 Getting Started

### Prerequisites

- K3s cluster running and accessible
- `kubectl` configured against your cluster
- ArgoCD installed in the cluster
- Docker Hub account with push access
- GitHub repository with Actions enabled

### 1 — Clone the Repository

```bash
git clone https://github.com/jaya-prakash-s-devops/kubernetes-devops-task-platform.git
cd kubernetes-devops-task-platform
```

### 2 — Create the Application Namespace

```bash
kubectl create namespace devops-platform
```

### 3 — Configure Kubernetes Secrets

```bash
kubectl create secret generic backend-secret \
  --from-literal=DB_PASSWORD=<your-db-password> \
  -n devops-platform
```

### 4 — Register the App in ArgoCD

```bash
kubectl apply -f argocd/application.yml
```

ArgoCD will detect the manifests in the repository and automatically sync the full application stack to the cluster.

### 5 — Add GitHub Actions Secrets

In your GitHub repository go to **Settings → Secrets → Actions** and add:

| Secret | Value |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub access token |

### 6 — Verify the Deployment

```bash
kubectl get all -n devops-platform
```

Expected: 3 backend pods, 3 frontend pods, 1 MySQL pod — all `Running` with 0 restarts.

---

## 📸 Screenshots

### Application — Login Page

![Application Login Page](docs/screenshots/application-login-page.png)

---

### Application — Task Dashboard

![Application Dashboard](docs/screenshots/application-dashboard.png)

---

### ArgoCD — GitOps Sync Status

> App Health: **Healthy** · Sync Status: **Synced** to `production-v2` · Auto-sync: **Enabled**

![ArgoCD GitOps Sync](docs/screenshots/screenshots-argocd-gitops-sync.png)

---

### Kubernetes Resources

> 3 backend pods · 3 frontend pods · 1 MySQL pod · All `Running` · 0 restarts

![Kubernetes Resources](docs/screenshots/kubernetes-resources.png)

---

### Prometheus — Backend Targets

> All 3 backend pod endpoints scraped and **UP** via ServiceMonitor

![Prometheus Backend Targets](docs/screenshots/prometheus-backend-targets.png)

---

### Prometheus — MySQL Target

> MySQL Exporter endpoint scraped and **UP**

![Prometheus MySQL Target](docs/screenshots/prometheus-mysql-target.png)

---

### Prometheus — Cluster Monitoring

> kube-state-metrics and Node Exporter both **UP**

![Prometheus Cluster Monitoring](docs/screenshots/prometheus-cluster-monitoring.png)

---

### Prometheus — Core Services

> Prometheus self-monitoring endpoints **UP**

![Prometheus Core Services](docs/screenshots/prometheus-core-services.png)

---

### Grafana — Infrastructure Health Dashboard

> Node memory ~80% · CPU tracked · 3 backend pods healthy

![Grafana Infrastructure Health](docs/screenshots/grafana-infrastructure-health.png)

---

### Grafana — Application Metrics Dashboard

> 2,590 total requests · 100% success rate · 0 errors · Response time within bounds

![Grafana Application Metrics](docs/screenshots/grafana-application-metrics.png)

---

### Grafana — Cluster and Database Health Dashboard

> 22/22 pods running · MySQL UP · Database connectivity: 1 · Cluster health: 1

![Grafana Cluster Database Health](docs/screenshots/grafana-cluster-database-health.png)

---

### Grafana — Database Performance Dashboard

> MySQL queries/sec stable · 7 active connections · 17,906 seconds uptime

![Grafana Database Performance](docs/screenshots/grafana-database-performance.png)

---

## 🎯 Key Achievements

- Designed and deployed a multi-tier application on a self-managed K3s Kubernetes cluster
- Implemented GitOps with ArgoCD enabling automatic, self-healing deployments
- Built an end-to-end GitHub Actions CI pipeline with automatic image tagging and manifest updates
- Configured Prometheus with ServiceMonitors for automatic metrics discovery across all services
- Built four custom Grafana dashboards covering infrastructure, application, cluster, and database health
- Applied Kubernetes production best practices — health probes, secrets management, PVCs, namespace isolation, and rolling updates

---

## 👤 Author

**Jaya Prakash S** — Junior DevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-jaya--prakash--s--devops-181717?style=flat-square&logo=github)](https://github.com/jaya-prakash-s-devops)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-jaya--prakash--s--devops-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/jaya-prakash-s-devops)

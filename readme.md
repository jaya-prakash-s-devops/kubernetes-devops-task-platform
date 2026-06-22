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
| Node | Node Exporter (9100) | CPU %, memory % |
| Kubernetes | kube-state-metrics | Pod count, deployment health |

### Grafana Dashboards

| Dashboard | Key Metrics |
|---|---|
| **Infrastructure Health** | Node CPU/Memory %, Backend pod count |
| **Application Metrics** | Total requests (2,590+), Success rate (100%), Error rate (0) |
| **Cluster & Database Health** | 22/22 pods running, MySQL up, Cluster health: 1 |
| **Database Performance** | MySQL queries/sec, 7 connections, 17,906s uptime |

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
│       ├── deploy.yml
│       └── deploy-ci-only.yml
├── argocd/
│   └── application.yml
├── backend/
├── backend-src/
├── frontend/
├── frontend-src/
├── k8/
├── mysql/
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
└── screenshots/
    ├── login-page.png
    ├── application-dashboard.png
    ├── github-actions-success.png
    ├── dockerhub-images.png
    ├── kubernetes-deployment.png
    ├── prometheus-targets.png
    └── grafana-dashboard.png
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

### 5 — Verify the Deployment

```bash
kubectl get all -n devops-platform
```

Expected: 3 backend pods, 3 frontend pods, 1 MySQL pod — all `Running` with 0 restarts.

---

## 📸 Screenshots

### Application — Login Page

![Login Page](screenshots/login-page.png)

---

### Application — Task Dashboard

![Application Dashboard](screenshots/application-dashboard.png)

---

### GitHub Actions — CI Pipeline Success

![GitHub Actions Success](screenshots/github-actions-success.png)

---

### Docker Hub — Published Images

![Docker Hub Images](screenshots/dockerhub-images.png)

---

### Kubernetes — Running Resources

![Kubernetes Deployment](screenshots/kubernetes-deployment.png)

---

### Prometheus — Scrape Targets

![Prometheus Targets](screenshots/prometheus-targets.png)

---

### Grafana — Monitoring Dashboard

![Grafana Dashboard](screenshots/grafana-dashboard.png)

---

## 🎯 Key Achievements

- Designed and deployed a multi-tier application on a self-managed K3s Kubernetes cluster
- Implemented GitOps with ArgoCD enabling automatic, self-healing deployments
- Built an end-to-end GitHub Actions CI pipeline with automatic image tagging and manifest updates
- Configured Prometheus with ServiceMonitors for automatic metrics discovery across all services
- Built custom Grafana dashboards covering infrastructure, application, cluster, and database health
- Applied Kubernetes production best practices — health probes, secrets management, PVCs, namespace isolation, and rolling updates

---

## 👤 Author

**Jaya Prakash S** — Junior DevOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-jaya--prakash--s--devops-181717?style=flat-square&logo=github)](https://github.com/jaya-prakash-s-devops)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-jaya--prakash--s--devops-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/jaya-prakash-s-devops)

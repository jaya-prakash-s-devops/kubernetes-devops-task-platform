# ⚙️ DevOps Task Platform

<div align="center">

![Platform](https://img.shields.io/badge/Platform-Kubernetes%20%28K3s%29-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitOps](https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python%20Flask-3776AB?style=flat-square&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

**A full-stack task management application deployed on a K3s Kubernetes cluster using GitOps principles — demonstrating containerization, orchestration, automated CI/CD, and production-grade observability.**

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

---

## 🔍 Overview

The **DevOps Task Platform** is a portfolio project built to demonstrate core DevOps engineering practices in a realistic, end-to-end environment. It features a simple full-stack task management application — but the real focus is the infrastructure around it:

- **Containerization** with Docker for consistent, reproducible builds
- **Kubernetes orchestration** on a self-managed K3s cluster with namespace isolation, health probes, and replica-based deployments
- **GitOps deployment** via ArgoCD with automatic sync and self-healing
- **Automated CI pipeline** with GitHub Actions that builds, pushes, and updates image tags on every commit
- **Full observability stack** using Prometheus, Grafana, Node Exporter, and MySQL Exporter with custom dashboards

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Developer Workflow                        │
│                                                                  │
│   git push  →  GitHub Actions  →  Docker Hub  →  Manifest Update│
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       GitOps (ArgoCD)                            │
│            Watches Git repo → Syncs to K3s cluster              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    K3s Kubernetes Cluster                         │
│                                                                  │
│  Namespace: devops-platform        Namespace: monitoring         │
│  ┌────────────────────────────┐   ┌─────────────────────────┐   │
│  │  frontend  (3 replicas)    │   │  Prometheus             │   │
│  │  backend   (3 replicas)    │   │  Grafana                │   │
│  │  mysql     (1 replica)     │   │  Alertmanager           │   │
│  │  ConfigMaps / Secrets      │   │  Node Exporter          │   │
│  │  PVC for MySQL             │   │  MySQL Exporter         │   │
│  └────────────────────────────┘   │  ServiceMonitors        │   │
│                                   └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python Flask |
| **Database** | MySQL |
| **Containerization** | Docker |
| **Orchestration** | K3s Kubernetes |
| **GitOps** | ArgoCD |
| **CI Pipeline** | GitHub Actions |
| **Monitoring** | Prometheus, Grafana, Node Exporter, MySQL Exporter |
| **Alerting** | Alertmanager |

---

## ✅ Application Features

- **User Registration** — Create a new account
- **User Login / Logout** — Session-based authentication
- **Task Creation** — Add tasks with a description
- **Task Management** — View and manage all tasks
- **Status Tracking** — Track tasks as `Pending`, `In Progress`, or `Completed`
- **Filtered Views** — Filter the task list by status

---

## 🔄 GitOps Workflow

```
Developer → git push → GitHub Repository
                              │
                              ▼
                      GitHub Actions CI
                      ├── Build frontend Docker image
                      ├── Build backend Docker image
                      ├── Push images to Docker Hub
                      └── Update image tags in K8s manifests
                              │
                              ▼
                      GitHub Repository (updated manifests)
                              │
                              ▼
                          ArgoCD
                      ├── Detects manifest diff
                      ├── Auto-syncs to K3s cluster
                      └── Reconciles desired vs actual state
                              │
                              ▼
                      K3s Cluster (updated deployment)
```

ArgoCD continuously reconciles the cluster state against the Git repository. If any resource drifts from the declared state, ArgoCD automatically corrects it — providing **self-healing** behavior without manual intervention.

---

## ☸️ Kubernetes Infrastructure

### Workloads

| Resource | Name | Replicas |
|---|---|---|
| Deployment | `backend` | 3 |
| Deployment | `frontend` | 3 |
| Deployment | `mysql` | 1 |

### Services

| Service | Type | Ports |
|---|---|---|
| `frontend-service` | NodePort | 80:30080 |
| `backend-service` | NodePort | 5000:30500 |
| `mysql` | ClusterIP | 3306, 9104 |

### Key Features Used

- **Namespace isolation** — Application and monitoring in separate namespaces
- **Deployments** — Declarative replica management with rolling updates
- **ConfigMaps** — Externalized application configuration
- **Secrets** — Sensitive values (DB credentials) stored securely
- **Persistent Volume Claim** — MySQL data persisted across pod restarts
- **Readiness Probes** — Traffic only routed to healthy pods
- **Liveness Probes** — Unhealthy pods automatically restarted
- **Rolling Updates** — Zero-downtime deployments via ArgoCD sync

---

## ⚙️ CI Pipeline

```
Trigger: push to main
  │
  ├── Step 1: Build frontend Docker image
  ├── Step 2: Build backend Docker image
  ├── Step 3: Push both images to Docker Hub
  └── Step 4: Update image tags in Kubernetes manifests
              └── Commit updated manifests back to repo
                  └── ArgoCD picks up the change automatically
```

The pipeline uses the Git commit SHA as the Docker image tag, ensuring every deployment is fully traceable back to a specific commit.

---

## 📊 Monitoring and Observability

### Metrics Scraping Targets

| Target | Exporter | Metrics Collected |
|---|---|---|
| Backend pods | Prometheus built-in | Request rate, response time, error rate, success % |
| MySQL | MySQL Exporter (port 9104) | Queries/sec, connections, uptime |
| K3s Node | Node Exporter (port 9100) | CPU %, memory % |
| Kubernetes | kube-state-metrics | Pod count, deployment health |
| Prometheus | Self-scrape | Prometheus internals |

### Grafana Dashboards

| Dashboard | Key Metrics |
|---|---|
| **Infrastructure Health** | Node CPU/Memory %, Backend pod count |
| **Application Metrics** | Total requests (2,590+), Success rate (100%), Error rate (0) |
| **Cluster & Database Health** | 22/22 pods running, MySQL up, Cluster healthy |
| **Database Performance** | MySQL queries/sec, 7 connections, 17,906s uptime |

---

## 📁 Project Structure

```
k8-project-folder/
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
│   │   ├── alertmanager-values.yml
│   │   ├── backend-alerts.yml
│   │   ├── mysql-alerts.yml
│   │   └── test-alert.yml
│   ├── backend-service-monitor.yml
│   ├── mysql-service-monitor.yml
│   └── values.yml
└── docs/
```

---

## 🚀 Getting Started

### Prerequisites

- K3s cluster running
- `kubectl` configured to point at your cluster
- ArgoCD installed in the cluster
- Docker Hub account
- GitHub repository with Actions enabled

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/devops-task-platform.git
cd devops-task-platform
```

### 2. Configure Secrets

```bash
kubectl create namespace devops-platform

kubectl create secret generic backend-secret \
  --from-literal=DB_PASSWORD=<your-db-password> \
  -n devops-platform
```

### 3. Register the App in ArgoCD

```bash
kubectl apply -f argocd/application.yml
```

### 4. Set GitHub Actions Secrets

In your GitHub repository settings, add the following secrets:

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub password or access token |

### 5. Verify Deployment

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

> App Health: **Healthy** | Sync Status: **Synced** to `production-v2` | Auto-sync: **Enabled**

![ArgoCD GitOps Sync](docs/screenshots/screenshots-argocd-gitops-sync.png)

---

### Kubernetes Resources

> All pods running with 0 restarts — 3 backend, 3 frontend, 1 MySQL.

![Kubernetes Resources](docs/screenshots/kubernetes-resources.png)

---

### Prometheus — Backend Targets

> All 3 backend pod endpoints scraped and **UP** via ServiceMonitor.

![Prometheus Backend Targets](docs/screenshots/prometheus-backend-targets.png)

---

### Prometheus — MySQL Target

> MySQL Exporter endpoint scraped and **UP**.

![Prometheus MySQL Target](docs/screenshots/prometheus-mysql-target.png)

---

### Prometheus — Cluster Monitoring

> kube-state-metrics and Node Exporter both **UP**.

![Prometheus Cluster Monitoring](docs/screenshots/prometheus-cluster-monitoring.png)

---

### Prometheus — Core Services

> Prometheus self-monitoring endpoints **UP**.

![Prometheus Core Services](docs/screenshots/prometheus-core-services.png)

---

### Grafana — Infrastructure Health Dashboard

> Node memory ~80%, CPU usage tracked, 3 backend pods healthy.

![Grafana Infrastructure Health](docs/screenshots/grafana-infrastructure-health.png)

---

### Grafana — Application Metrics Dashboard

> 2,590 total requests | 100% success rate | 0 errors

![Grafana Application Metrics](docs/screenshots/grafana-application-metrics.png)

---

### Grafana — Cluster and Database Health Dashboard

> 22/22 pods running | MySQL UP | Database connectivity: 1 | Cluster health: 1

![Grafana Cluster Database Health](docs/screenshots/grafana-cluster-database-health.png)

---

### Grafana — Database Performance Dashboard

> MySQL queries/sec stable | 7 active connections | 17,906 seconds uptime

![Grafana Database Performance](docs/screenshots/grafana-database-performance.png)

---

## 🎯 Key Takeaways

This project demonstrates the ability to:

- Containerize a multi-service application with Docker
- Deploy and manage workloads on a self-managed Kubernetes cluster (K3s)
- Implement GitOps with ArgoCD for declarative, automated deployment
- Build a CI pipeline with GitHub Actions producing tagged, traceable Docker images
- Configure a full observability stack (Prometheus + Grafana + exporters) with custom dashboards
- Apply Kubernetes best practices: health probes, secrets management, PVCs, namespace isolation, and rolling updates

---

<div align="center">

Made by **Jayaprakash** · Junior DevOps Engineer

</div>

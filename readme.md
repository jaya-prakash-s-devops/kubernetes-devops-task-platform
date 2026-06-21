# DevOps Task Platform

A production-style DevOps project demonstrating GitOps-based Kubernetes deployment using ArgoCD, automated CI/CD with GitHub Actions, containerization using Docker, monitoring with Prometheus and Grafana, and a full-stack task management application.

---

## Project Overview

The DevOps Task Platform is a multi-tier web application deployed on Kubernetes using K3s.

The project demonstrates:

- Docker containerization
- Kubernetes orchestration
- GitHub Actions CI pipeline
- GitOps deployment with ArgoCD
- Prometheus monitoring
- Grafana dashboards
- MySQL database integration
- Automated image version management
- Self-healing Kubernetes deployments

---

# Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions CI
(Build & Push Images)
    │
    ▼
Docker Hub
    │
    ▼
Update Kubernetes Manifests
    │
    ▼
Git Repository
    │
    ▼
ArgoCD
    │
    ▼
K3s Kubernetes Cluster
    │
 ┌──┴──┐
 ▼     ▼
Frontend Backend
          │
          ▼
        MySQL

Monitoring Stack

Prometheus
     │
     ▼
Grafana
```

---

# Technology Stack

## Cloud & Infrastructure

- AWS EC2
- K3s Kubernetes
- Docker
- Docker Hub

## CI/CD & GitOps

- GitHub Actions
- ArgoCD
- Git
- GitHub

## Monitoring

- Prometheus
- Grafana
- Node Exporter
- MySQL Exporter
- ServiceMonitors

## Application

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask

### Database

- MySQL

---

# GitOps Workflow

1. Developer pushes code to GitHub.
2. GitHub Actions builds backend and frontend Docker images.
3. Images are pushed to Docker Hub.
4. GitHub Actions automatically updates Kubernetes image tags.
5. Updated manifests are committed back to GitHub.
6. ArgoCD detects repository changes.
7. ArgoCD automatically synchronizes the Kubernetes cluster.
8. New application version is deployed.
9. Prometheus and Grafana monitor application health.

---

# CI/CD Features

### GitHub Actions

- Automated image build
- Docker Hub image push
- Automatic image tag generation
- Automatic Kubernetes manifest update
- GitOps integration

### ArgoCD

- Automatic synchronization
- Self-healing
- Automated deployment
- GitOps-based state management

---

# Project Screenshots

## Application Login Page

User authentication page.

![Application Login](screenshots/application-login-page.png)

---

## Application Dashboard

Task management dashboard showing task tracking and CRUD operations.

![Application Dashboard](screenshots/application-dashboard.png)

---

## ArgoCD GitOps Deployment

ArgoCD automatically synchronizing Kubernetes resources from Git.

Features:

- Healthy status
- Synced status
- Automatic deployment
- Self-healing

![ArgoCD GitOps](screenshots/argocd-gitops-sync.png)

---

## Kubernetes Resources

Running Kubernetes resources inside the cluster.

Features:

- Backend deployment
- Frontend deployment
- MySQL deployment
- Services
- ReplicaSets

![Kubernetes Resources](screenshots/kubernetes-resources.png)

---

## Prometheus Backend Monitoring

Prometheus scraping backend application metrics.

Features:

- Backend ServiceMonitor
- Multiple backend replicas
- Metrics collection

![Prometheus Backend Targets](screenshots/prometheus-backend-targets.png)

---

## Prometheus MySQL Monitoring

Monitoring MySQL through MySQL Exporter.

![Prometheus MySQL Target](screenshots/prometheus-mysql-target.png)

---

## Prometheus Cluster Monitoring

Prometheus monitoring internal cluster services.

![Prometheus Cluster Monitoring](screenshots/prometheus-cluster-monitoring.png)

---

## Prometheus Core Services

Cluster observability services.

Features:

- Node Exporter
- Kube State Metrics

![Prometheus Core Services](screenshots/prometheus-core-services.png)

---

## Grafana Infrastructure Dashboard

Infrastructure monitoring dashboard.

Metrics:

- CPU Usage
- Memory Usage
- Backend Pod Availability

![Infrastructure Health](screenshots/grafana-infrastructure-health.png)

---

## Grafana Application Dashboard

Application monitoring dashboard.

Metrics:

- Request Rate
- Response Time
- Success Rate
- Total Requests

![Application Metrics](screenshots/grafana-application-metrics.png)

---

## Grafana Cluster & Database Health Dashboard

Cluster and database health monitoring.

Metrics:

- Running Pods
- Cluster Health
- Database Status
- Database Connectivity

![Cluster Database Health](screenshots/grafana-cluster-database-health.png)

---

## Grafana Database Performance Dashboard

Database performance monitoring.

Metrics:

- MySQL Queries/sec
- MySQL Connections
- MySQL Uptime
- Database Error Rate

![Database Performance](screenshots/grafana-database-performance.png)

---

# Kubernetes Resources

Application Namespace:

```bash
devops-platform
```

Deployments:

```bash
backend
frontend
mysql
```

Services:

```bash
backend-service
frontend-service
mysql
```

Monitoring Components:

```bash
Prometheus
Grafana
Node Exporter
MySQL Exporter
ServiceMonitors
AlertManager
```

---

# Deployment Instructions

## Clone Repository

```bash
git clone https://github.com/jaya-prakash-s-devops/kubernetes-devops-task-platform.git

cd kubernetes-devops-task-platform
```

## Deploy Application

```bash
kubectl apply -f .
```

## Deploy ArgoCD Application

```bash
kubectl apply -f argocd/application.yml
```

## Verify Resources

```bash
kubectl get all -n devops-platform
```

---

# Monitoring Access

## Grafana

```text
http://<NODE-IP>:30080
```

## Prometheus

```text
http://<NODE-IP>:30090
```

## ArgoCD

```text
http://<NODE-IP>:8080
```

---

# Key Achievements

- Implemented GitOps deployment with ArgoCD
- Automated CI pipeline using GitHub Actions
- Automated Kubernetes image updates
- Built a multi-tier Kubernetes application
- Implemented Prometheus monitoring
- Built Grafana dashboards
- Configured MySQL monitoring
- Configured Kubernetes observability
- Implemented self-healing deployments
- Managed rolling application updates

---

# Author

**Jaya Prakash S**

- GitHub: https://github.com/jaya-prakash-s-devops
- LinkedIn: https://www.linkedin.com/in/jaya-prakash-s-devops

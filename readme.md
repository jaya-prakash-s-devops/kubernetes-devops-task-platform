# 🚀 Production-Grade GitOps DevOps Task Management Platform

A production-style GitOps Kubernetes platform demonstrating modern DevOps practices including containerization, CI automation, GitOps deployment, Kubernetes orchestration, monitoring, observability, and automated application delivery.

The platform deploys a full-stack Task Management Application consisting of:

- Frontend (NGINX)
- Backend API (Flask)
- MySQL Database

The application is containerized using Docker, built automatically using GitHub Actions, published to Docker Hub, and deployed to a K3s Kubernetes cluster using ArgoCD GitOps workflows.

---

# 📌 Key Features

## GitOps Deployment

- ArgoCD Continuous Delivery
- Automatic Kubernetes Manifest Updates
- Git as Single Source of Truth
- Self-Healing Deployments
- Automated Synchronization

## CI Automation

- GitHub Actions Pipeline
- Automated Docker Builds
- Docker Hub Publishing
- Automatic Image Tag Management

## Kubernetes

- K3s Cluster
- Deployments
- Services
- ConfigMaps
- Secrets
- Persistent Volume Claims
- Rolling Updates
- Multi-Replica Deployments

## Monitoring & Observability

- Prometheus
- Grafana
- Alertmanager
- Node Exporter
- Kube State Metrics
- MySQL Exporter
- Custom Flask Metrics

---

# 🏗️ Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
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
 ┌──┼─────────────┐
 ▼  ▼             ▼
Frontend       Backend       MySQL
(NGINX)        (Flask)
                    │
                    ▼
            Prometheus
                    │
                    ▼
               Grafana
                    │
                    ▼
              Alertmanager
```

---

# 🛠️ Technology Stack

## Containerization

- Docker

## GitOps & CI/CD

- GitHub Actions
- ArgoCD
- Docker Hub

## Kubernetes

- K3s
- Deployments
- Services
- ConfigMaps
- Secrets
- PVC
- Ingress

## Monitoring

- Prometheus
- Grafana
- Alertmanager
- ServiceMonitor
- Node Exporter
- Kube State Metrics
- MySQL Exporter

## Application

- Python Flask
- MySQL
- HTML
- CSS
- JavaScript
- NGINX

---

# 🔄 GitOps Workflow

```text
Developer Pushes Code
        │
        ▼
GitHub Actions Triggered
        │
        ▼
Build Backend Image
Build Frontend Image
        │
        ▼
Push Images To Docker Hub
        │
        ▼
Update deployment.yml Image Tags
        │
        ▼
Commit Changes Back To Git
        │
        ▼
ArgoCD Detects Changes
        │
        ▼
Automatic Sync
        │
        ▼
Rolling Deployment To K3s
```

---

# 📂 Project Structure

```text
.
├── .github
│   └── workflows
│       └── deploy.yml
│
├── argocd
│   └── application.yml
│
├── backend
│   ├── configmap.yml
│   ├── deployment.yml
│   ├── secret.yml
│   └── service.yml
│
├── backend-src
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── deployment.yml
│   └── service.yml
│
├── frontend-src
│   ├── Dockerfile
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── mysql
│   ├── deployment.yml
│   ├── pvc.yml
│   ├── secret.yml
│   └── service.yml
│
├── ingress
│   └── ingress.yml
│
├── k8
│   └── namespace.yml
│
├── monitoring
│   ├── alertmanager
│   ├── alerts
│   ├── backend-service-monitor.yml
│   ├── mysql-service-monitor.yml
│   ├── values.yml
│   └── alertmanager-values.yml
│
└── screenshots
```

---

# ☸️ Kubernetes Resources

Current Deployment:

- Backend Deployment (3 Replicas)
- Frontend Deployment (3 Replicas)
- MySQL Deployment (1 Replica)
- ConfigMaps
- Secrets
- Persistent Storage (PVC)
- NodePort Services
- ArgoCD Application
- Prometheus Monitoring Stack
- Grafana Dashboards
- Alertmanager Configuration

---

# 📊 Monitoring & Observability

Prometheus Scrapes:

- Backend Application Metrics
- MySQL Metrics
- Node Exporter Metrics
- Kubernetes Metrics
- Kube State Metrics

Grafana Dashboards Include:

### Infrastructure Health

- Node CPU Usage
- Node Memory Usage

### Application Health

- Backend Pods Availability
- Backend Replica Status

### Database Health

- MySQL Availability
- Database Connectivity

### Traffic Metrics

- Total Requests
- Backend Request Rate

### Performance Metrics

- Backend Response Time
- Backend Success Rate
- Backend Error Rate

### Database Performance

- MySQL Queries per Second
- MySQL Connections
- MySQL Uptime

---

# 📸 Screenshots

## Application Login Page

```md
![Application Login](screenshots/application-login-page.png)
```

## Application Dashboard

```md
![Application Dashboard](screenshots/application-dashboard.png)
```

## Infrastructure Health Dashboard

```md
![Infrastructure Health](screenshots/grafana-infrastructure-health.png)
```

## Application Metrics Dashboard

```md
![Application Metrics](screenshots/grafana-application-metrics.png)
```

## Cluster & Database Health Dashboard

```md
![Cluster Database Health](screenshots/grafana-cluster-database-health.png)
```

## Database Performance Dashboard

```md
![Database Performance](screenshots/grafana-database-performance.png)
```

## Kubernetes Resources

```md
![Kubernetes Resources](screenshots/kubernetes-resources.png)
```

## ArgoCD GitOps Synchronization

```md
![ArgoCD GitOps Sync](screenshots/argocd-gitops-sync.png)
```

## Prometheus Backend Targets

```md
![Prometheus Backend Targets](screenshots/prometheus-backend-targets.png)
```

## Prometheus MySQL Targets

```md
![Prometheus MySQL Target](screenshots/prometheus-mysql-target.png)
```

## Prometheus Cluster Monitoring

```md
![Prometheus Cluster Monitoring](screenshots/prometheus-cluster-monitoring.png)
```

## Prometheus Core Services

```md
![Prometheus Core Services](screenshots/prometheus-core-services.png)
```

---

# ⚙️ GitHub Actions CI Pipeline

Workflow Steps:

1. Checkout Repository
2. Generate Image Tag
3. Login To Docker Hub
4. Build Backend Image
5. Push Backend Image
6. Build Frontend Image
7. Push Frontend Image
8. Update Kubernetes Manifests
9. Commit Updated Image Tags
10. Push Changes To GitHub

This enables a complete GitOps workflow where image updates are automatically reflected in Kubernetes manifests.

---

# 🚀 ArgoCD GitOps Deployment

ArgoCD continuously watches the `production-v2` branch.

When GitHub Actions updates image tags:

```yaml
image: jsdaya2211/backend-image:da7a217
image: jsdaya2211/frontend:da7a217
```

ArgoCD automatically:

- Detects Manifest Changes
- Syncs The Application
- Performs Rolling Updates
- Maintains Desired State
- Self-Heals Drift

No manual deployment commands are required.

---

# ✅ Deployment Verification

Successfully Running:

- Frontend Deployment (3 Pods)
- Backend Deployment (3 Pods)
- MySQL Deployment (1 Pod)
- ArgoCD
- Prometheus
- Grafana
- Alertmanager
- Node Exporter
- Kube State Metrics

Prometheus Targets:

- Backend Monitor → UP
- MySQL Monitor → UP
- Node Exporter → UP
- Kube State Metrics → UP
- Prometheus Service → UP

ArgoCD Status:

- Healthy
- Synced
- Auto Sync Enabled
- Self Heal Enabled

---

# 🎯 Learning Outcomes

This project demonstrates hands-on experience with:

- Docker Containerization
- GitHub Actions Automation
- Docker Hub Registry
- K3s Kubernetes
- Kubernetes Deployments
- Services
- ConfigMaps
- Secrets
- Persistent Storage
- GitOps Workflows
- ArgoCD
- Prometheus Monitoring
- Grafana Dashboards
- Alertmanager
- ServiceMonitor
- MySQL Exporter
- Rolling Deployments
- Infrastructure Monitoring
- Kubernetes Troubleshooting
- Production-Style DevOps Practices

---

# 🚀 Future Improvements

- Horizontal Pod Autoscaler (HPA)
- Cert-Manager TLS Certificates
- Multi-Node K3s Cluster
- Slack Alert Notifications
- Backup & Disaster Recovery
- Centralized Logging (ELK/Loki)
- Helm Chart Packaging

---

# 👨‍💻 Author

**Jaya Prakash S**

GitHub: https://github.com/jaya-prakash-s-devops

LinkedIn: https://www.linkedin.com/in/jaya-prakash-s-devops

# 📸 Project Screenshots

## 1. Application Login Page

The user authentication page for accessing the DevOps Task Platform.

![Application Login](screenshots/application-login-page.png)

---

## 2. Task Management Dashboard

Main application dashboard showing task creation, task status tracking and CRUD operations.

![Application Dashboard](screenshots/application-dashboard.png)

---

## 3. GitOps Deployment with ArgoCD

ArgoCD continuously monitors the Git repository and automatically synchronizes Kubernetes resources when changes are detected.

Features demonstrated:

- Healthy Application State
- Synced Status
- Automatic Deployment
- GitOps Workflow
- Self-Healing Capability

![ArgoCD GitOps](screenshots/argocd-gitops-sync.png)

---

## 4. Kubernetes Cluster Resources

Verification of running Kubernetes workloads.

Resources shown:

- Backend Deployment (3 Replicas)
- Frontend Deployment (3 Replicas)
- MySQL Database
- Services
- ReplicaSets
- Namespace Resources

![Kubernetes Resources](screenshots/kubernetes-resources.png)

---

## 5. Prometheus Backend Monitoring

Prometheus successfully scraping metrics from all backend application pods.

Features demonstrated:

- ServiceMonitor Integration
- Backend Metrics Collection
- Multi-Pod Monitoring

![Prometheus Backend Targets](screenshots/prometheus-backend-targets.png)

---

## 6. Prometheus MySQL Monitoring

Prometheus collecting database metrics through MySQL Exporter.

Features demonstrated:

- Database Metrics Collection
- MySQL Exporter Integration

![Prometheus MySQL](screenshots/prometheus-mysql-target.png)

---

## 7. Prometheus Cluster Monitoring

Monitoring of Prometheus services and cluster observability components.

Features demonstrated:

- Prometheus Health
- Cluster Monitoring Components

![Prometheus Cluster Monitoring](screenshots/prometheus-cluster-monitoring.png)

---

## 8. Core Kubernetes Monitoring Services

Infrastructure monitoring services used by Prometheus.

Features demonstrated:

- Kube State Metrics
- Node Exporter
- Kubernetes Cluster Metrics

![Prometheus Core Services](screenshots/prometheus-core-services.png)

---

## 9. Infrastructure Health Dashboard

Grafana dashboard visualizing node-level metrics.

Metrics monitored:

- CPU Usage
- Memory Usage
- Backend Pod Availability
- Replica Health

![Infrastructure Health](screenshots/grafana-infrastructure-health.png)

---

## 10. Application Performance Dashboard

Grafana dashboard showing application traffic and performance metrics.

Metrics monitored:

- Total Requests
- Request Rate
- Response Time
- Success Rate

![Application Metrics](screenshots/grafana-application-metrics.png)

---

## 11. Cluster & Database Health Dashboard

Grafana dashboard showing Kubernetes and MySQL health status.

Metrics monitored:

- Database Availability
- Database Connectivity
- Total Pods
- Running Pods
- Cluster Health

![Cluster Database Health](screenshots/grafana-cluster-database-health.png)

---

## 12. Database Performance Dashboard

Grafana dashboard for MySQL performance monitoring.

Metrics monitored:

- MySQL Queries per Second
- MySQL Connections
- MySQL Uptime
- Database Error Rate

![Database Performance](screenshots/grafana-database-performance.png)

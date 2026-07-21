# Real-Time Chat Infrastructure & EKS GitOps Pipeline

![AWS EKS](https://img.shields.io/badge/AWS-EKS-orange?logo=amazon-aws)
![Docker](https://img.shields.io/badge/Docker-Containers-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes)
![Jenkins](https://img.shields.io/badge/Jenkins-CD__Pipeline-D24939?logo=jenkins)
![GitHub Actions](https://img.shields.io/badge/GitHub__Actions-CI-2088FF?logo=github-actions)
![SonarQube](https://img.shields.io/badge/SonarQube-Code__Quality-4E9BCD?logo=sonarqube)

A high-availability, containerized real-time chat application architecture deployed on **Amazon EKS** with dual-stage CI/CD automation, static code analysis, and dynamic infrastructure environment configuration.

---

## 📐 Architecture Overview

```text
 [ Developer Commit ] 
          │
          ▼
   [ GitHub Actions CI ] ────► ( Unit Tests & Linting ) ────► [ SonarQube Code Quality ]
          │                                                               │
          ▼                                                               ▼
   [ Build Docker Image ] ───► [ Docker Hub (Tagged with Git SHA) ] ───► [ Jenkins CD ]
                                                                          │
                                                                          ▼
                                                                [ AWS EKS Deployment ]
                                                                 ├── Nginx Frontend
                                                                 ├── Node.js Backend
                                                                 └── Amazon RDS MySQL
```

## Key Engineering Highlights
Immutable Commit-Based Tagging: Every CI execution builds and tags Docker images with the exact Git Commit SHA, guaranteeing full auditability and zero-downtime rollbacks.
.
├── .github/workflows/      # Automated CI workflow definition
├── backend/                 # Node.js + Socket.io backend API & tests
├── html/                    # React SPA frontend & Nginx config
├── k8s/                     # Kubernetes manifests (Deployments, Services, ConfigMaps)
├── Dockerfile               # Multi-stage production container builds
├── docker-compose.yml       # Local development orchestration
├── Jenkinsfile              # Continuous Deployment pipeline script
└── SonarQube-DockerCompose.yml # Static analysis environment setup
Dual-Environment Database Abstraction: Flexible backend runtime design using SQLite for local development and Amazon RDS MySQL for production.

Kubernetes Orchestration: Decoupled deployment model using Kubernetes ConfigMaps for environment variables and Secrets for database credentials.

Real-time Stateful Sockets: Scalable WebSocket management via Socket.io backed by Node.js.

## 🛠 Tech Stack
Frontend: React.js, Vite, Nginx, Docker

Backend: Node.js, Express.js, Socket.io, Jest, Docker

Database: SQLite (Dev), Amazon RDS MySQL (Prod)

Infrastructure & CI/CD: AWS EKS, AWS EC2, Jenkins, GitHub Actions, Docker Compose, SonarQube, eksctl, kubectl

## 📂 Project Structure
```text
.
├── .github/workflows/      # Automated CI workflow definition
├── backend/                 # Node.js + Socket.io backend API & tests
├── html/                    # React SPA frontend & Nginx config
├── k8s/                     # Kubernetes manifests (Deployments, Services, ConfigMaps)
├── Dockerfile               # Multi-stage production container builds
├── docker-compose.yml       # Local development orchestration
├── Jenkinsfile              # Continuous Deployment pipeline script
└── SonarQube-DockerCompose.yml # Static analysis environment setup
```


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

## 🚀 Local Development Setup
1. Run via Docker Compose (Recommended)
```Bash
# Spin up both backend and frontend environments locally
docker-compose up -d --build
```
Access the application at http://localhost:3000.

2. Manual Bare-Metal Setup
```Bash
# Install and run backend
cd backend
npm install
npm run dev


# In a new terminal, install and run frontend
cd html
npm install
npm run dev
```
## 🔄 CI/CD & Deployment Pipeline
Continuous Integration (GitHub Actions)
Trigger: Pull Requests and Pushes to the main branch.

Quality Checks: Runs unit testing suites via Jest.

Security & Code Quality: Integrates with SonarQube for static analysis.

Registry Build: Builds multi-stage Docker images and pushes them to Docker Hub with latest and ${GITHUB_SHA} tags.

Continuous Deployment (Jenkins & EKS)
Agent Setup: Jenkins runner executes deployment scripts.

Cluster Authentication: Configures AWS credentials and establishes active context with AWS EKS.

Dynamic Patching: Dynamically replaces container image tags in k8s/ manifests using the specific commit SHA.

Rollout Verification: Deploys manifests and verifies deployment status using kubectl rollout status.

## ☁️ Amazon EKS Deployment Guide
Prerequisites
AWS CLI configured with administrator privileges (aws configure)

eksctl and kubectl installed on host runner

Step 1: Create EKS Cluster
```Bash
eksctl create cluster \
  --name EKSCHAT \
  --region ap-south-1 \
  --nodegroup-name default-ng \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 2 \
  --managed
```
Step 2: Apply Kubernetes Resources
```Bash
# Create secrets for MySQL DB connection
kubectl apply -f k8s/secret.yaml

# Deploy Backend & Frontend Microservices
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```
## 🧪 Testing
```Bash
# Execute unit and integration tests
cd backend
npm test

# Generate coverage report
npm run test:coverage
```

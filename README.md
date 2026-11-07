# Nexora AI — Full-Stack Educational & AI Research Platform

[![Platform](https://img.shields.io/badge/Platform-Nexora%20AI-6366F1)](https://github.com/Darshan-yadav-45/Nexora)
[![Java](https://img.shields.io/badge/Java-21%20LTS-ED8B00?logo=openjdk&logoColor=white)](https://openjdk.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3.5-6DB33F?logo=springboot&logoColor=white)](https://spring.io/projects/spring-boot)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

Nexora AI is a production-grade, AI-powered learning and research ecosystem featuring:
- **Central Authority Java Spring Boot Backend** for authentication, authorization, dynamic education profiles, and data access.
- **Dedicated Python FastAPI AI Microservice** for source-grounded RAG, human-readable writing improvements, and 20 Research Studio analytical tools.
- **Dynamic Student Education Journey** covering SSLC/10th, PUC/12th, Diploma, Undergraduate, Postgraduate, and PhD qualifications.
- **NotebookLM-Style 3-Panel AI Research Notebook** with exact page-level source citations and inline studio exports.
- **Structured Career Roadmaps** with comprehensive modules, practical exercises, and interview preparation for Java Full Stack, Python Full Stack, and Data Analysis.
- **Modern Responsive React 19 UI** styled with Tailwind CSS.

---

## 🏗 Architecture Overview

```
Frontend (React 19 / TypeScript / Tailwind CSS - Port 5173)
                   │
                   ▼  (Bearer JWT over HTTPS)
┌───────────────────────────────────────────────────────────────────┐
│ Java Spring Boot 3.3.5 (Primary Backend Authority - Port 8000)    │
│  • Spring Security with Stateless JWT & BCrypt (Factor 12)        │
│  • Central Authority: Auth, Education Profiles, Notebooks, Social │
│  • Spring Data JPA / Hibernate Relational Persistence             │
└────────┬──────────────────────────────────────────┬───────────────┘
         │                                          │  Service-to-Service REST
         │  PostgreSQL Port 5434                    │  Headers:
         ▼                                          │   X-Internal-Service-Key
┌─────────────────────────────────────────┐         │   X-User-Id / X-User-Email
│ PostgreSQL 17 Database                  │         ▼
│  • 77 Relational Tables                 │ ┌───────────────────────────────┐
│  • pgvector Semantic Storage            │ │ Python FastAPI AI Microservice│
│  • Flyway Migrations                    │ │ (Internal - Port 8001)        │
└─────────────────────────────────────────┘ │  • Grounded RAG Citations     │
                                            │  • Writing Humanizer          │
                                            │  • 20 Research Studio Tools   │
                                            └───────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Java 21 LTS** or compatible JDK
- **Apache Maven 3.9+**
- **Python 3.12+**
- **Node.js 18+** & npm
- **PostgreSQL 17** (listening on port `5434` or configured in `application.properties`)

---

### 2. Database Setup
Create database `voxalearn`:
```sql
CREATE DATABASE voxalearn;
```

---

### 3. Start Python AI Microservice (Port 8001)

**On Windows (PowerShell):**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

*(Or run directly without activation: `.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001`)*

**On Linux / macOS:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

---

### 4. Start Java Spring Boot Primary Backend (Port 8000)
```bash
cd backend-java
mvn clean package -DskipTests
java -jar target/nexora-backend-2.5.0.jar
```
*Or with Maven plugin:*
```bash
mvn spring-boot:run
```

---

### 5. Start React Frontend (Port 5173)
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🔒 Security Architecture
- **Argon2id / BCrypt** password hashing (`cost factor 12`).
- **HMAC-SHA256 JWT tokens** with role and user context verification.
- **Service-to-Service Protection**: Python microservice requires `X-Internal-Service-Key` and verified `X-User-Id`; direct frontend access is rejected with `403 Forbidden`.
- **Zero Frontend Trust**: Frontend client never communicates directly with internal AI processes or database instances.


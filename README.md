# 🚀 Transaction Analytics AI Service

An AI-powered microservices backend system for transaction analytics, intelligent financial reporting, and document-based question answering using RAG (Retrieval-Augmented Generation).

This project combines:

- FastAPI microservices
- AI-generated financial insights
- RAG-based semantic document querying
- MySQL + FAISS vector database
- Ollama + Llama3 integration
- Dockerized architecture
- Background document processing
- Metrics and logging support

---

# 📌 Project Overview

This project is designed as a production-style AI backend platform.

The system provides:

✅ Transaction CRUD APIs  
✅ AI-powered analytics  
✅ RAG-based document intelligence  
✅ Async background processing  
✅ Dockerized services  
✅ Metrics & monitoring  
✅ Logging & error handling  

The platform uses LLMs to analyze financial data and generate human-readable insights.

---

# 🧠 Core Features

# ✅ CRUD Transaction APIs

Perform complete transaction management:

- Create transactions
- Fetch all transactions
- Fetch transaction by ID
- Update transactions
- Delete transactions

---

# ✅ AI-Powered Financial Reporting

Generate intelligent financial insights using LLMs.

Supported AI reports:

- Spending summaries
- Category insights
- Trend analysis
- Failure analysis
- Natural language explanations

Powered by:

- Ollama
- Llama3
- Prompt Engineering

---

# ✅ RAG-Based Document Intelligence

Upload documents and ask questions using natural language.

Supported formats:

- PDF
- TXT
- CSV

RAG workflow:

1. Upload document
2. Parse and chunk text
3. Generate embeddings
4. Store vectors in FAISS
5. Retrieve relevant chunks
6. Generate contextual AI response

---

# ✅ Async Background Processing

Large document processing runs asynchronously using:

- FastAPI BackgroundTasks

Benefits:

- Faster API responses
- Improved scalability
- Better user experience

---

# ✅ Logging

Implemented centralized logging for:

- API requests
- Errors
- AI processing
- File uploads

---

# ✅ Metrics & Monitoring

Prometheus-compatible metrics endpoint:

```bash
/metrics
```

Tracks:

- Request count
- API latency
- Response timing
- Monitoring statistics

---

# 🏗️ System Architecture

```text
                +----------------+
                |     Client     |
                +----------------+
                         |
                         v
              +--------------------+
              |    API Service     |
              |      FastAPI       |
              +--------------------+
                 |            |
                 |            |
                 v            v
         +------------+   +-------------------+
         |   MySQL    |   | AI Report Service |
         +------------+   +-------------------+
                                   |
                                   |
                         +------------------+
                         |     Ollama       |
                         |     Llama3       |
                         +------------------+
                                   |
                                   v
                         +------------------+
                         |    FAISS Vector  |
                         |      Database    |
                         +------------------+

Worker Service handles:
- document parsing
- chunking
- embedding generation
- background processing
```

---

# 📂 Project Structure

```bash
transaction-ai-service/
│
├── api-service/
│   ├── main.py
│   ├── crud.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── ai_client.py
│   ├── logger.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── ai-report-service/
│   ├── main.py
│   ├── service.py
│   ├── database.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── rag/
│       ├── ingestion/
│       ├── embeddings/
│       └── retrieval/
│
├── worker-service/
│   ├── worker.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

# 🧰 Tech Stack

# Backend

- FastAPI
- SQLAlchemy
- Pydantic
- MySQL

---

# AI & RAG

- Ollama
- Llama3
- LangChain
- FAISS
- HuggingFace Embeddings
- Sentence Transformers

---

# DevOps

- Docker
- Docker Compose

---

# ⚙️ Installation & Setup

# 1️⃣ Clone Repository

```bash
git clone <your-repository-url>
cd transaction-ai-service
```

---

# 2️⃣ Start Docker Desktop

Ensure Docker Desktop is running.

---

# 3️⃣ Build & Start Services

```bash
docker compose up --build
```

---

# 🌐 Services & Ports

| Service | Port |
|---|---|
| API Service | 8000 |
| AI Report Service | 8001 |
| MySQL | 3306 |

---

# 📌 API Endpoints

# Transaction APIs

| Method | Endpoint |
|---|---|
| POST | `/api/v1/records` |
| GET | `/api/v1/records` |
| GET | `/api/v1/records/{id}` |
| PUT | `/api/v1/records/{id}` |
| DELETE | `/api/v1/records/{id}` |

---

# 🤖 AI Reporting APIs

| Endpoint | Description |
|---|---|
| `/api/v1/ai-summary/{user_id}` | AI-generated summary |
| `/api/v1/ai-category-insights/{user_id}` | Category insights |
| `/api/v1/ai-trend/{user_id}` | Trend analysis |
| `/api/v1/ai-failures/{user_id}` | Failure analysis |

---

# 📚 RAG APIs

| Endpoint | Description |
|---|---|
| `/rag/upload` | Upload document |
| `/rag/query` | Ask questions from uploaded documents |

---

# 📈 Metrics Endpoint

```bash
GET /metrics
```

---

# 📄 Swagger Documentation

# API Service

```bash
http://localhost:8000/docs
```

# AI Report Service

```bash
http://localhost:8001/docs
```

---

# ✅ Validation Implemented

- Amount must be greater than 0
- Status validation (`success` / `failed`)
- Category validation
- File type validation for uploads

---

# ⚠️ Edge Cases Handled

- Empty datasets
- Invalid uploads
- Missing RAG results
- Validation failures
- Database connection issues
- AI service failures

---

# 🔄 RAG Workflow

```text
Upload Document
       ↓
Document Parsing
       ↓
Chunking
       ↓
Embedding Generation
       ↓
FAISS Vector Storage
       ↓
Semantic Retrieval
       ↓
LLM Response Generation
```

---

# 🧠 AI Processing Workflow

```text
Transaction Data
       ↓
Preprocessing
       ↓
Prompt Engineering
       ↓
LLM Analysis (Llama3)
       ↓
AI-generated Insights
```

---

# 🐳 Dockerized Architecture

Each service runs independently inside Docker containers.

Benefits:

- Isolated environments
- Dependency management
- Easy deployment
- Production-style architecture

---

# ⭐ Conclusion

This project demonstrates:

- Backend Development
- AI Integration
- RAG Architecture
- Dockerization
- Async Processing
- Logging & Monitoring
- Production-style System Design

The platform is designed as a scalable and production-oriented AI backend system.

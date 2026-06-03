
```markdown
# Multi-Document RAG Base (v1.1)

A robust, local Retrieval-Augmented Generation (RAG) system built with Next.js, FastAPI, PostgreSQL (`pgvector`), and Ollama. This setup allows you to upload multiple PDF documents, process and embed them locally, and perform context-aware semantic searches to answer user queries.

---

## 🏗️ System Architecture


```

User
│
▼
Frontend (Next.js)
│
▼
FastAPI Backend
├── PDF Upload API
├── Chat API (RAG)
├── Embedding Service (Ollama)
└── LLM Service (Ollama)
│
▼
PostgreSQL + pgvector
│
▼
Vector Similarity Search
│
▼
Context ──> LLM ──> Answer

```

---

## 🚀 Features

### 📄 PDF Upload & Processing
* **Endpoint:** `POST /upload`
* **Text Extraction:** Powered by `pypdf`.
* **Text Sanitization:** Automatic cleaning of invalid/control characters.
* **Chunking:** Fixed-size chunking with strategic overlap.
* **Vector Storage:** Embeddings are generated locally and stored directly in PostgreSQL.

### 🧠 RAG Pipeline

```

PDF ──> Text Extraction ──> Chunking ──> Cleaning ──> Embeddings ──> Vector DB

```

### 💬 Chat System
* **Endpoint:** `POST /chat`
* **Flow:**

```

User Query ──> Embedding (Ollama) ──> Vector Search (pgvector) ──> Top-K Context ──> Prompt Construction ──> LLM (llama3.2)

```

---

## 🛠️ Tech Stack & Configurations

### 🤖 AI Models (Ollama)
* **Embedding Model:** `nomic-embed-text` (Generates 768-dimensional dense vectors used for semantic search).
* **LLM Model:** `llama3.2` (Handles context-aware answer generation).

### ✂️ Chunking Strategy
* **Chunk Size:** 1000 characters
* **Chunk Overlap:** 200 characters
* **Why:** Balances granular semantic data retrieval with enough surrounding context to prevent information loss at chunk boundaries.

### 🧹 Text Cleaning (Critical Step)
To prevent database serialization errors during insertion, the backend automatically sanitizes extracted text before embedding:
* Removes `NULL` bytes (`\x00`).
* Strips invalid control characters.
* Normalizes whitespace.

---

## 🗄️ Database Schema

The system uses PostgreSQL with the `pgvector` extension to handle relational metadata and high-dimensional vector data side-by-side.

```sql
-- Track uploaded files
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  document_id TEXT UNIQUE,
  filename TEXT,
  file_type TEXT DEFAULT 'pdf',
  upload_time TIMESTAMP DEFAULT NOW()
);

-- Store document chunks and their high-dimensional embeddings
CREATE TABLE document_chunks (
  id SERIAL PRIMARY KEY,
  document_id TEXT REFERENCES documents(document_id) ON DELETE CASCADE,
  chunk_index INT,
  content TEXT,
  embedding VECTOR(768)
);

```

### 🔎 Vector Search Logic

The system utilizes **Euclidean Distance (`<->`)** (or optionally Cosine Distance `<=>`) to fetch the top 5 most relevant chunks:

```sql
SELECT content 
FROM document_chunks 
ORDER BY embedding <-> :query_embedding 
LIMIT 5;

```

---

## 📌 API Endpoints Reference

### 1. Upload PDF

* **Method:** `POST`
* **Path:** `/upload`
* **Payload:** `multipart/form-data` (File)

**Response:**

```json
{
  "document_id": "8f3b29c1-a842-4d73-b391-729019e1e54c",
  "filename": "architecture_guide.pdf",
  "status": "processed"
}

```

### 2. Chat with Document

* **Method:** `POST`
* **Path:** `/chat`

**Request Body:**

```json
{
  "message": "Tell me about software architecture"
}

```

**Response Body:**

```json
{
  "response": "Based on the provided documents, software architecture refers to..."
}

```

---

## ⚠️ Known Limitations (v1.1)

1. **Global Vector Space:** There is currently no multi-tenant or per-document filtering logic. All uploaded documents share the same global vector space during retrieval.
2. **Stateless Chat:** No session-based chat memory is implemented. Every query is processed independently without historical conversation context.
3. **Basic Retrieval:** The search pipeline relies entirely on basic vector similarity. Advanced techniques like metadata filtering, hybrid search (BM25 + Vector), or cross-encoder reranking are not yet supported.
4. **Fixed Chunking:** Document splitting is purely character-bound; it does not account for natural semantic boundaries (e.g., paragraphs or markdown headers).

```

```

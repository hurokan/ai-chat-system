# AI Chat System

A local Retrieval-Augmented Generation (RAG) system built using FastAPI, Ollama, PostgreSQL (pgvector), and Next.js.

---

# Architecture Overview

```text
┌─────────────┐
│  Frontend   │
│   Next.js   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   FastAPI   │
│   Backend   │
└──────┬──────┘
       │
       ├──────────────┐
       │              │
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│ PostgreSQL  │  │   Ollama    │
│ + pgvector  │  │ Local LLM   │
└─────────────┘  └─────────────┘
```

---

# Tech Stack

## Frontend

* Next.js
* React

## Backend

* FastAPI
* Uvicorn
* Requests

## AI Components

* Ollama
* llama3.2
* nomic-embed-text

## Database

* PostgreSQL
* pgvector

## Infrastructure

* Docker
* Docker Compose

---

# Current Features

## PDF Upload

Users can upload PDF documents.

Endpoint:

```http
POST /upload
```

Workflow:

1. Upload PDF
2. Extract text using pypdf
3. Split text into chunks
4. Generate embeddings
5. Store chunks in PostgreSQL

---

## Embedding Generation

Model:

```text
nomic-embed-text
```

API:

```http
POST /api/embeddings
```

Example:

```json
{
  "model": "nomic-embed-text",
  "prompt": "Software Architecture"
}
```

Embedding size:

```text
768 dimensions
```

---

## Vector Database

Table:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    document_id TEXT,
    filename TEXT,
    chunk_index INT,
    content TEXT,
    embedding VECTOR(768)
);
```

---

## Chat Endpoint

Endpoint:

```http
POST /chat
```

Request:

```json
{
  "message": "Tell me about software architecture"
}
```

Response:

```json
{
  "response": "Generated answer..."
}
```

---

# Current RAG Pipeline

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Build Context
      │
      ▼
LLM (llama3.2)
      │
      ▼
Generated Answer
```

---

# Current Models

## Embedding Model

```text
nomic-embed-text
```

Purpose:

* Semantic Search
* Similarity Matching
* Vector Retrieval

---

## LLM

```text
llama3.2
```

Purpose:

* Question Answering
* Summarization
* Context-Aware Responses

---

# Understanding Context Window

Current configuration:

```text
n_ctx = 4096
```

Meaning:

The model can process approximately:

```text
3000–3500 words
```

per request.

---

# Why RAG Is Needed

A book may contain:

```text
200,000+ tokens
```

But the model can only process:

```text
4096 tokens
```

Therefore:

```text
Book
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Search
 ↓
Relevant Chunks
 ↓
LLM
```

Only the most relevant information is sent to the model.

---

# Docker Services

Current containers:

```text
frontend
backend
postgres
redis
ollama
litellm
```

# Project Status

### Implemented

* PDF Upload
* Text Extraction
* Chunking
* Embedding Generation
* Vector Storage
* Similarity Search
* Basic RAG
* Dockerized Deployment

---

# Known Limitations

## Retrieval Quality

Current implementation:

* Fixed chunk size
* No chunk overlap
* Top-K vector retrieval only

Missing:

* Hybrid Search
* Reranking
* Metadata Filtering

---

## Multi-Document Issues

Currently all documents share the same vector space.

Potential issue:

```text
Question about Book A
↓
Retrieval returns chunks from CV.pdf
↓
Incorrect answer
```

Solution:

```text
Document Metadata
+
Document Filtering
```

---

## Chat Memory

Not implemented.

Current flow:

```text
Question
↓
Retrieve
↓
Answer
```

No conversation history is stored.


# Current System Flow

```text
PDF Upload
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Embedding Generation
    │
    ▼
PostgreSQL + pgvector
    │
    ▼
Question
    │
    ▼
Vector Search
    │
    ▼
Relevant Chunks
    │
    ▼
llama3.2
    │
    ▼
Answer
```

---


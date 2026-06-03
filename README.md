v1.1 - Stable Multi-Document RAG Base

User
 │
 ▼
Frontend (Next.js)
 │
 ▼
FastAPI Backend
 │
 ├── PDF Upload API
 ├── Chat API (RAG)
 │
 ├── Embedding Service (Ollama)
 ├── LLM Service (Ollama)
 │
 ▼
PostgreSQL + pgvector
 │
 ▼
Vector Similarity Search
 │
 ▼
Context → LLM → Answer

Features (v1.1)
📄 PDF Upload
Upload PDF via /upload
Extract text using pypdf
Clean invalid characters
Split into chunks
Generate embeddings
Store in PostgreSQL

🧠 RAG Pipeline
PDF → Text Extraction → Chunking → Cleaning → Embeddings → Vector DB

💬 Chat System

Endpoint:

POST /chat

Flow:

User Query
   ↓
Embedding (Ollama)
   ↓
Vector Search (pgvector)
   ↓
Top-K Context Retrieval
   ↓
Prompt Construction
   ↓
LLM Response (llama3.2)
🗄️ Database Schema
📄 documents
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    document_id TEXT UNIQUE,
    filename TEXT,
    file_type TEXT DEFAULT 'pdf',
    upload_time TIMESTAMP DEFAULT NOW()
);
🧩 document_chunks
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id TEXT,
    chunk_index INT,
    content TEXT,
    embedding VECTOR(768)
);
🧠 Embedding Model
nomic-embed-text
Used for semantic search
Converts text → vector (768-dim)
🤖 LLM Model
llama3.2
Used for answering questions
Context-aware generation
✂️ Chunking Strategy
size = 1000 characters
overlap = 200 characters

Why:

improves retrieval accuracy
avoids losing context
🧹 Text Cleaning (IMPORTANT)

Before storing in DB:

Remove NULL bytes (\x00)
Remove control characters
Normalize whitespace
🔎 Vector Search Logic
SELECT content
FROM document_chunks
ORDER BY embedding <-> query_embedding
LIMIT 5;

📌 API Endpoints
Upload PDF
POST /upload

Response:

{
  "document_id": "uuid",
  "filename": "file.pdf",
  "status": "processed"
}
Chat with Document
POST /chat

Request:

{
  "message": "Tell me about software architecture"
}

Response:

{
  "response": "AI generated answer..."
}
⚠️ Known Limitations
1. No document filtering

All documents share vector space.

2. No chat memory

Each query is independent.

3. Basic retrieval only
No reranking
No hybrid search
4. Simple chunking
Fixed size
No semantic splitting
📘 AI Chat System — RAG Backend (v1.1)

A lightweight Retrieval-Augmented Generation (RAG) system built with FastAPI + PostgreSQL (pgvector) + Ollama LLM, designed for document-based question answering.

🏗️ 1. Current Architecture
🔄 High-Level Flow
User → Frontend → FastAPI Backend
                 ↓
            Embedding Service (Ollama)
                 ↓
        PostgreSQL (pgvector search)
                 ↓
         Top-K Relevant Chunks
                 ↓
          Prompt Builder (RAG)
                 ↓
            Ollama LLM (LLama3)
                 ↓
            AI Response
                

🧩 Core Components
1. FastAPI Backend
Handles /upload and /chat
Manages RAG pipeline orchestration
2. Ollama (LLM + Embeddings)
Embedding model: nomic-embed-text
Chat model: llama3.2
Runs locally in Docker
3. PostgreSQL + pgvector
Stores:
documents
document_chunks
Performs vector similarity search using <->
4. RAG Pipeline
Chunk document
Generate embeddings
Store in DB
Retrieve top-k chunks
Send to LLM

🎯 2. Scope of Current System
✅ What it supports
PDF document upload
Text extraction from PDFs
Chunking (fixed size)
Vector embeddings via Ollama
Semantic search using pgvector
Single-document QA
Basic RAG prompt injection
REST API (/upload, /chat)

📌 Use Cases
Document Q&A chatbot
Internal knowledge assistant
PDF summarization system
Basic enterprise search

⚠️ 3. Limitations (Current Version)
❌ Architecture Limitations
No multi-document filtering
No session-based memory
No reranking layer
No hybrid search (keyword + vector)
Fixed chunking strategy (no token-aware chunking)
No streaming response (non-streaming chat)
No context optimization (token overflow risk)
❌ Data Limitations
No document versioning
No metadata filtering
No chunk-level ranking score tuning
❌ LLM Limitations
No prompt optimization engine
No memory context window manager
No tool-calling / agent layer

🚀 4. How to Run (Docker + DB Setup)
📦 Step 1 — Clone Project
git clone <repo-url>
cd ai-chat-system


🐳 Step 2 — Start Full Stack
docker compose up --build

This will start:

Backend (FastAPI)
PostgreSQL (with pgvector)
Ollama (LLM runtime)
Frontend (Next.js)

🗄️ Step 3 — Run Database Migrations

After containers start:

docker exec -it backend python migrate.py

📄 Step 4 — Enable pgvector (if needed)

Inside Postgres:

CREATE EXTENSION IF NOT EXISTS vector;
📤 Step 5 — Upload Document
POST /upload

Upload PDF file → system will:

extract text
chunk it
store embeddings
💬 Step 6 — Chat with Document
POST /chat

Request:

{
  "message": "Tell me about the document"
}


🧠 5. Technology Stack (and Why)
⚙️ Backend: FastAPI (Python)
Why:
Lightweight & fast
Async support
Ideal for AI APIs
Easy integration with ML services
🧠 LLM: Ollama
Why:
Runs models locally
No OpenAI dependency
Supports LLaMA models
Fast inference inside Docker
🧮 Embeddings: nomic-embed-text
Why:
High-quality semantic embeddings
Lightweight compared to OpenAI embeddings
Works offline
🗄️ Database: PostgreSQL + pgvector
Why:
Production-grade relational DB
pgvector enables vector similarity search
Scalable for enterprise RAG systems
📄 Parsing: PyPDF
Why:
Simple PDF extraction
Works well for text-based documents
🐳 Docker
Why:
Full environment reproducibility
Easy deployment
Isolated services (DB, backend, LLM)
🌐 Frontend: Next.js
Why:
React-based UI framework
Fast rendering
Easy API integration
Ideal for ChatGPT-like UI

🔮 Future Roadmap (v1.2 → v2.0)
🚀 Planned Improvements
Multi-document RAG
Session-based chat memory
Streaming responses (ChatGPT-like)
Hybrid search (BM25 + Vector)
Reranking model layer
Token-aware chunking
Context compression engine
API authentication layer

🧠 Summary

This system is a:

Lightweight but extensible RAG foundation built for production evolution.

It is designed to gradually evolve into:

OpenAI / LangChain-style production RAG architecture
            

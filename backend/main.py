from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import requests
import json
import os
import psycopg2

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CONFIG
# =========================
OLLAMA_CHAT_URL = "http://ollama:11434/api/generate"
OLLAMA_EMBED_URL = "http://ollama:11434/api/embeddings"

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# DB CONNECTION HELPER
# =========================
def get_conn():
    return psycopg2.connect(
        host="postgres",
        database="ai_chat",
        user="admin",
        password="admin123"
    )


# =========================
# VECTOR HELPER (IMPORTANT FIX)
# =========================
def to_vector_string(vec):
    return "[" + ",".join(map(str, vec)) + "]"


# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str


# =========================
# EMBEDDINGS (OLLAMA)
# =========================
def get_embedding(text: str):
    res = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return res.json()["embedding"]


# =========================
# UPLOAD PDF
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    print("🔥 UPLOAD STARTED")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # extract text
    from pypdf import PdfReader

    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text

    print("TOTAL TEXT LENGTH:", len(text))

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    print("CHUNKS:", len(chunks))

    conn = get_conn()
    cur = conn.cursor()

    inserted = 0

    for chunk in chunks:
        try:
            embedding = get_embedding(chunk)

            cur.execute(
                "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                (chunk, to_vector_string(embedding))
            )

            inserted += 1

        except Exception as e:
            print("❌ INSERT ERROR:", e)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ INSERTED ROWS:", inserted)

    return {
        "chunks": len(chunks),
        "inserted": inserted
    }


# =========================
# CHAT (RAG ENABLED)
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    try:
        conn = get_conn()
        cur = conn.cursor()

        # 1. embed query
        query_embedding = get_embedding(req.message)

        # 2. vector search (FIXED)
        cur.execute("""
            SELECT content
            FROM documents
            ORDER BY embedding <-> %s::vector
            LIMIT 3
        """, (to_vector_string(query_embedding),))

        rows = cur.fetchall()

        context = "\n".join([r[0] for r in rows])

        cur.close()
        conn.close()

        # 3. build prompt
        prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{req.message}
"""

        # 4. call ollama
        response = requests.post(
            OLLAMA_CHAT_URL,
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        return {
            "response": data.get("response", "")
        }

    except Exception as e:
        print("❌ CHAT ERROR:", e)
        return {"error": str(e)}
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import requests
import psycopg2
from pypdf import PdfReader

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
# DB
# =========================
def get_conn():
    return psycopg2.connect(
        host="postgres",
        database="ai_chat",
        user="admin",
        password="admin123"
    )

# =========================
# VECTOR FORMAT
# =========================
def to_vector(v):
    return "[" + ",".join(map(str, v)) + "]"

# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    message: str
    document_id: str | None = None

# =========================
# EMBEDDING
# =========================
def embed(text):
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

    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(path)

    text = ""
    for p in reader.pages:
        text += p.extract_text() or ""

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    conn = get_conn()
    cur = conn.cursor()

    for i, chunk in enumerate(chunks):
        try:
            vec = embed(chunk)

            cur.execute("""
                INSERT INTO documents
                (document_id, filename, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                file.filename,
                file.filename,
                i,
                chunk,
                to_vector(vec)
            ))

        except Exception as e:
            conn.rollback()
            print("ERROR:", e)

        else:
            conn.commit()

    cur.close()
    conn.close()

    return {
        "document_id": file.filename,
        "chunks": len(chunks)
    }

# =========================
# CHAT (RAG)
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    conn = get_conn()
    cur = conn.cursor()

    qvec = embed(req.message)

    # If document_id provided → filtered search
    if req.document_id:
        cur.execute("""
            SELECT content
            FROM documents
            WHERE document_id = %s
            ORDER BY embedding <-> %s::vector
            LIMIT 5
        """, (req.document_id, to_vector(qvec)))
    else:
        cur.execute("""
            SELECT content
            FROM documents
            ORDER BY embedding <-> %s::vector
            LIMIT 5
        """, (to_vector(qvec),))

    rows = cur.fetchall()

    context = "\n".join([r[0] for r in rows])

    prompt = f"""
Use only the context below.

Context:
{context}

Question:
{req.message}
"""

    res = requests.post(
        OLLAMA_CHAT_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    cur.close()
    conn.close()

    return {
        "response": res.json().get("response", "")
    }
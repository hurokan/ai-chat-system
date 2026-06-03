from fastapi import APIRouter, UploadFile, File
import uuid
from pypdf import PdfReader
from services.ingestion_service import ingest_document
from db.connection import get_conn

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    document_id = str(uuid.uuid4())

    reader = PdfReader(file.file)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    # save metadata
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO documents (document_id, filename)
        VALUES (%s, %s)
    """, (document_id, file.filename))

    conn.commit()
    cur.close()
    conn.close()

    # ingest chunks
    ingest_document(document_id, file.filename, text)

    return {
        "document_id": document_id,
        "filename": file.filename
    }

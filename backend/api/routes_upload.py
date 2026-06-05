from fastapi import APIRouter, UploadFile, File
from services.ingestion_service import ingest_document
from pypdf import PdfReader
import tempfile

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    document_id = ingest_document(file.filename, text)

    return {
        "document_id": document_id,
        "status": "uploaded"
    }

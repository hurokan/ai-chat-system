from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ingestion_service import ingest_document
from pypdf import PdfReader
import tempfile

router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF allowed")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        reader = PdfReader(tmp_path)

        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)

        full_text = "\n".join(pages_text).strip()

        if not full_text:
            raise HTTPException(status_code=400, detail="No extractable text found")

        document_id = ingest_document(file.filename, full_text)

        return {
            "document_id": document_id,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
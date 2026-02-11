from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_storage import save_pdf
from app.services.pdf_reader import extract_raw_text_from_pdf
from app.services.memory_store import (
    store_company_document,
    store_bank_document
)

router = APIRouter(prefix="/documents", tags=["Documents"])


# Upload Company PDF

@router.post("/company/upload")
async def upload_company_pdf(file: UploadFile = File(...)):

    try:
        file_path = save_pdf(file)
        raw_text = extract_raw_text_from_pdf(file_path)

        document_id = store_company_document(
            text=raw_text,
            file_path=file_path
        )

        return {
            "document_id": document_id,
            "document_type": "company",
            "status": "uploaded_and_extracted"
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Upload Bank PDF


@router.post("/bank/upload")
async def upload_bank_pdf(file: UploadFile = File(...)):

    try:
        file_path = save_pdf(file)
        raw_text = extract_raw_text_from_pdf(file_path)

        document_id = store_bank_document(
            text=raw_text,
            file_path=file_path
        )

        return {
            "document_id": document_id,
            "document_type": "bank",
            "status": "uploaded_and_extracted"
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

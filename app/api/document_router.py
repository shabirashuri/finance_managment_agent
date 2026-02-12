from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_storage import save_pdf
from app.services.pdf_reader import extract_raw_text_from_pdf
from app.services.document_service import create_document

router = APIRouter(prefix="/documents", tags=["Documents"])


# Upload Company PDF
@router.post("/company/upload")
async def upload_company_pdf(file: UploadFile = File(...)):

    try:
        file_path = save_pdf(file)
        raw_text = extract_raw_text_from_pdf(file_path)

        document_id = await create_document(
            document_type="company",
            raw_text=raw_text
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

        document_id = await create_document(
            document_type="bank",
            raw_text=raw_text
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

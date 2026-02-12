from fastapi import APIRouter, HTTPException
from app.services.document_service import get_document, update_document
from app.services.ai_extractor import extract_company_cheques, extract_bank_cheques
from app.services.tally_engine import tally_cheques

router = APIRouter(prefix="/full_tally", tags=["Full Tally"])


@router.post("/{company_id}/{bank_id}")
async def full_tally(company_id: str, bank_id: str):

    company_doc = await get_document(company_id)
    bank_doc = await get_document(bank_id)

    if not company_doc:
        raise HTTPException(status_code=404, detail="Company document not found")

    if not bank_doc:
        raise HTTPException(status_code=404, detail="Bank document not found")

    # Structure data using LLM
    company_structured = extract_company_cheques(company_doc["raw_text"])
    bank_structured = extract_bank_cheques(bank_doc["raw_text"])

    # Apply tally engine
    result = tally_cheques(company_structured, bank_structured)

    # Save structured + tally results in DB
    await update_document(company_id, {
        "structured_data": company_structured.dict(),
        "tally_result": result,
        "status": "tallied"
    })

    await update_document(bank_id, {
        "structured_data": bank_structured.dict(),
        "status": "structured"
    })

    return {
        "company_structured": company_structured.dict(),
        "bank_structured": bank_structured.dict(),
        "tally_result": result
    }

from fastapi import APIRouter, HTTPException, Depends, status
from app.services.document_service import get_document, update_document
from app.services.ai_extractor import extract_company_cheques, extract_bank_cheques
from app.services.tally_engine import tally_cheques
from app.services.session_service import get_session_by_id
from app.core.auth import get_current_user
import logging

router = APIRouter(prefix="/tally", tags=["Tally"])
logger = logging.getLogger(__name__)


@router.post("/{session_id}")
async def full_tally(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Perform full tally reconciliation for a session.
    
    Args:
        session_id: Session ID containing both company and bank documents
        current_user: Current authenticated user
        
    Returns:
        Tally results with structured data
    """
    try:
        # Get and validate session
        session = await get_session_by_id(session_id, current_user["user_id"])
        
        # Validate session has both documents
        if not session.get("company_document_id") or not session.get("bank_document_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session must have both company and bank documents uploaded"
            )
        
        # Get documents
        company_doc = await get_document(session["company_document_id"])
        bank_doc = await get_document(session["bank_document_id"])
        
        if not company_doc or not bank_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both documents not found"
            )
        
        # Structure data using LLM
        company_structured = extract_company_cheques(company_doc["raw_text"])
        bank_structured = extract_bank_cheques(bank_doc["raw_text"])
        
        logger.info(f"Tally endpoint - Company cheques: {len(company_structured.cheques)}, Bank cheques: {len(bank_structured.cashed_cheques)}")
        
        # Apply tally engine
        result = tally_cheques(company_structured, bank_structured)
        
        # Save structured + tally results in DB
        await update_document(session["company_document_id"], {
            "structured_data": company_structured.dict(),
            "tally_result": result,
            "status": "tallied"
        })
        
        await update_document(session["bank_document_id"], {
            "structured_data": bank_structured.dict(),
            "status": "structured"
        })
        
        return {
            "session_id": session_id,
            "company_structured": company_structured.dict(),
            "bank_structured": bank_structured.dict(),
            "tally_result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tally error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform tally: {str(e)}"
        )


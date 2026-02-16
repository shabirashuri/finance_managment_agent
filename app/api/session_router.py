from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
import logging
from app.schemas.session_schema import SessionCreate, SessionResponse, SessionList, DocumentUploadResponse
from app.services.session_service import (
    create_session,
    get_user_sessions,
    get_session_by_id,
    delete_session,
    update_session_document
)
from app.services.file_storage import save_pdf
from app.services.pdf_reader import extract_raw_text_from_pdf
from app.services.document_service import create_document
from app.core.auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])
logger = logging.getLogger(__name__)


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_session(
    session_data: SessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new session for the current user.
    
    Args:
        session_data: Session creation data (session_name)
        current_user: Current authenticated user
        
    Returns:
        Created session information
    """
    try:
        session = await create_session(current_user["user_id"], session_data)
        return SessionResponse(**session.model_dump())
        
    except Exception as e:
        logger.error(f"Session creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session"
        )


@router.get("", response_model=SessionList)
async def list_sessions(current_user: dict = Depends(get_current_user)):
    """
    Get all sessions for the current user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        List of user's sessions
    """
    try:
        sessions = await get_user_sessions(current_user["user_id"])
        
        session_responses = [SessionResponse(**session) for session in sessions]
        
        return SessionList(
            sessions=session_responses,
            total=len(session_responses)
        )
        
    except Exception as e:
        logger.error(f"Session listing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sessions"
        )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific session by ID.
    
    Args:
        session_id: Session ID
        current_user: Current authenticated user
        
    Returns:
        Session information
    """
    try:
        session = await get_session_by_id(session_id, current_user["user_id"])
        return SessionResponse(**session)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session"
        )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session_endpoint(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a session and its associated documents.
    
    Args:
        session_id: Session ID
        current_user: Current authenticated user
    """
    try:
        await delete_session(session_id, current_user["user_id"])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session deletion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete session"
        )


@router.post("/{session_id}/upload-company", response_model=DocumentUploadResponse)
async def upload_company_document(
    session_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a company document to a session.
    
    Args:
        session_id: Session ID
        file: PDF file to upload
        current_user: Current authenticated user
        
    Returns:
        Document upload information
    """
    try:
        # Save PDF and extract text
        file_path = save_pdf(file)
        raw_text = extract_raw_text_from_pdf(file_path)
        
        # Create document
        document_id = await create_document(
            user_id=current_user["user_id"],
            session_id=session_id,
            document_type="company",
            raw_text=raw_text
        )
        
        # Update session
        await update_session_document(
            session_id=session_id,
            user_id=current_user["user_id"],
            document_id=document_id,
            document_type="company"
        )
        
        return DocumentUploadResponse(
            document_id=document_id,
            session_id=session_id,
            document_type="company",
            status="uploaded_and_extracted"
        )
        
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Company document upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload company document"
        )


@router.post("/{session_id}/upload-bank", response_model=DocumentUploadResponse)
async def upload_bank_document(
    session_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a bank document to a session.
    
    Args:
        session_id: Session ID
        file: PDF file to upload
        current_user: Current authenticated user
        
    Returns:
        Document upload information
    """
    try:
        # Save PDF and extract text
        file_path = save_pdf(file)
        raw_text = extract_raw_text_from_pdf(file_path)
        
        # Create document
        document_id = await create_document(
            user_id=current_user["user_id"],
            session_id=session_id,
            document_type="bank",
            raw_text=raw_text
        )
        
        # Update session
        await update_session_document(
            session_id=session_id,
            user_id=current_user["user_id"],
            document_id=document_id,
            document_type="bank"
        )
        
        return DocumentUploadResponse(
            document_id=document_id,
            session_id=session_id,
            document_type="bank",
            status="uploaded_and_extracted"
        )
        
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Bank document upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload bank document"
        )

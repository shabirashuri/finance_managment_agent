from app.core.database import documents_collection, sessions_collection
from app.models.document_model import DocumentModel
from app.core.exceptions import SessionNotFoundError, SessionValidationError, AuthorizationError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def create_document(
    user_id: str,
    session_id: str,
    document_type: str,
    raw_text: str
) -> str:
    """
    Create a new document and associate it with a session.
    
    Args:
        user_id: ID of the user creating the document
        session_id: ID of the session to associate with
        document_type: Type of document ("bank" or "company")
        raw_text: Extracted text from PDF
        
    Returns:
        Document ID
        
    Raises:
        SessionNotFoundError: If session doesn't exist
        AuthorizationError: If user doesn't own the session
        SessionValidationError: If session already has this document type
    """
    # Validate session exists and belongs to user
    session = await sessions_collection.find_one({"session_id": session_id})
    if not session:
        raise SessionNotFoundError(session_id)
    
    if session["user_id"] != user_id:
        raise AuthorizationError("You don't have access to this session")
    
    # Check if session already has this document type
    field_name = f"{document_type}_document_id"
    if session.get(field_name):
        raise SessionValidationError(
            f"Session already has a {document_type} document"
        )
    
    # Create document
    document = DocumentModel(
        user_id=user_id,
        session_id=session_id,
        document_type=document_type,
        raw_text=raw_text
    )
    
    # Insert into database
    await documents_collection.insert_one(document.model_dump())
    
    logger.info(f"Created {document_type} document {document.document_id} for session {session_id}")
    
    return document.document_id


async def get_document(document_id: str):
    """Get document by ID."""
    return await documents_collection.find_one({"document_id": document_id})


async def update_document(document_id: str, update_data: dict):
    """Update document with new data."""
    update_data["updated_at"] = datetime.utcnow()
    
    await documents_collection.update_one(
        {"document_id": document_id},
        {"$set": update_data}
    )

from datetime import datetime
from typing import List, Optional
import logging
from app.core.database import sessions_collection, documents_collection
from app.core.exceptions import SessionNotFoundError, SessionValidationError, AuthorizationError
from app.models.session import SessionModel
from app.schemas.session_schema import SessionCreate

logger = logging.getLogger(__name__)


async def create_session(user_id: str, session_data: SessionCreate) -> SessionModel:
    """
    Create a new session for a user.
    
    Args:
        user_id: ID of the user creating the session
        session_data: Session creation data
        
    Returns:
        Created session model
    """
    session = SessionModel(
        user_id=user_id,
        session_name=session_data.session_name
    )
    
    await sessions_collection.insert_one(session.model_dump())
    
    logger.info(f"Created session {session.session_id} for user {user_id}")
    
    return session


async def get_user_sessions(user_id: str) -> List[dict]:
    """
    Get all sessions for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        List of session documents
    """
    cursor = sessions_collection.find({"user_id": user_id}).sort("created_at", -1)
    sessions = await cursor.to_list(length=None)
    
    return sessions


async def get_session_by_id(session_id: str, user_id: Optional[str] = None) -> dict:
    """
    Get session by ID with optional user validation.
    
    Args:
        session_id: Session ID
        user_id: Optional user ID to validate ownership
        
    Returns:
        Session document
        
    Raises:
        SessionNotFoundError: If session doesn't exist
        AuthorizationError: If user doesn't own the session
    """
    session = await sessions_collection.find_one({"session_id": session_id})
    
    if not session:
        raise SessionNotFoundError(session_id)
    
    # Validate ownership if user_id provided
    if user_id and session["user_id"] != user_id:
        raise AuthorizationError("You don't have access to this session")
    
    return session


async def update_session_document(
    session_id: str,
    user_id: str,
    document_id: str,
    document_type: str
) -> dict:
    """
    Associate a document with a session.
    
    Args:
        session_id: Session ID
        user_id: User ID (for validation)
        document_id: Document ID to associate
        document_type: Type of document ("company" or "bank")
        
    Returns:
        Updated session document
        
    Raises:
        SessionNotFoundError: If session doesn't exist
        AuthorizationError: If user doesn't own the session
        SessionValidationError: If session already has this document type
    """
    # Get and validate session
    session = await get_session_by_id(session_id, user_id)
    
    # Check if session already has this document type
    field_name = f"{document_type}_document_id"
    if session.get(field_name):
        raise SessionValidationError(
            f"Session already has a {document_type} document. Delete the session and create a new one."
        )
    
    # Determine new status
    if document_type == "company":
        if session.get("bank_document_id"):
            new_status = "complete"
        else:
            new_status = "company_uploaded"
    else:  # bank
        if session.get("company_document_id"):
            new_status = "complete"
        else:
            new_status = "bank_uploaded"
    
    # Update session
    update_data = {
        field_name: document_id,
        "status": new_status,
        "updated_at": datetime.utcnow()
    }
    
    await sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": update_data}
    )
    
    logger.info(f"Updated session {session_id} with {document_type} document {document_id}")
    
    # Return updated session
    return await get_session_by_id(session_id)


async def delete_session(session_id: str, user_id: str) -> bool:
    """
    Delete a session and its associated documents.
    
    Args:
        session_id: Session ID
        user_id: User ID (for validation)
        
    Returns:
        True if deleted successfully
        
    Raises:
        SessionNotFoundError: If session doesn't exist
        AuthorizationError: If user doesn't own the session
    """
    # Get and validate session
    session = await get_session_by_id(session_id, user_id)
    
    # Delete associated documents
    await documents_collection.delete_many({"session_id": session_id})
    
    # Delete session
    result = await sessions_collection.delete_one({"session_id": session_id})
    
    logger.info(f"Deleted session {session_id} and its documents")
    
    return result.deleted_count > 0


async def validate_session_ownership(session_id: str, user_id: str) -> bool:
    """
    Validate that a user owns a session.
    
    Args:
        session_id: Session ID
        user_id: User ID
        
    Returns:
        True if user owns session
        
    Raises:
        SessionNotFoundError: If session doesn't exist
        AuthorizationError: If user doesn't own the session
    """
    await get_session_by_id(session_id, user_id)
    return True

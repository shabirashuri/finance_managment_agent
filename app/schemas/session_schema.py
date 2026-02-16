from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime


class SessionCreate(BaseModel):
    """Schema for creating a new session."""
    session_name: str = Field(..., min_length=1, max_length=200)
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_name": "Q1 2024 Reconciliation"
            }
        }


class SessionResponse(BaseModel):
    """Schema for session response."""
    session_id: str
    user_id: str
    session_name: str
    company_document_id: Optional[str] = None
    bank_document_id: Optional[str] = None
    status: Literal["created", "company_uploaded", "bank_uploaded", "complete", "tallied"]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "123e4567-e89b-12d3-a456-426614174001",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "session_name": "Q1 2024 Reconciliation",
                "company_document_id": "doc-123",
                "bank_document_id": "doc-456",
                "status": "complete",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class SessionList(BaseModel):
    """Schema for list of sessions."""
    sessions: List[SessionResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "sessions": [
                    {
                        "session_id": "123e4567-e89b-12d3-a456-426614174001",
                        "user_id": "123e4567-e89b-12d3-a456-426614174000",
                        "session_name": "Q1 2024 Reconciliation",
                        "company_document_id": "doc-123",
                        "bank_document_id": "doc-456",
                        "status": "complete",
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": "2024-01-01T00:00:00"
                    }
                ],
                "total": 1
            }
        }


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    document_id: str
    session_id: str
    document_type: Literal["bank", "company"]
    status: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc-123",
                "session_id": "session-456",
                "document_type": "company",
                "status": "uploaded_and_extracted"
            }
        }

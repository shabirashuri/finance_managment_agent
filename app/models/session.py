from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import uuid4


class SessionModel(BaseModel):
    """Session database model for grouping documents."""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    session_name: str
    company_document_id: Optional[str] = None
    bank_document_id: Optional[str] = None
    status: Literal["created", "company_uploaded", "bank_uploaded", "complete", "tallied"] = "created"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
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

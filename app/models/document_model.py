from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime
from uuid import uuid4


class DocumentModel(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str  # Owner of the document
    session_id: str  # Session this document belongs to
    document_type: Literal["bank", "company"]

    raw_text: str

    structured_data: Optional[Dict[str, Any]] = None
    tally_result: Optional[Dict[str, Any]] = None

    status: Literal["uploaded", "structured", "tallied"] = "uploaded"

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


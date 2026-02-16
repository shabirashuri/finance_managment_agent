from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from uuid import uuid4


class UserModel(BaseModel):
    """User database model."""
    user_id: str = Field(default_factory=lambda: str(uuid4()))
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "johndoe",
                "hashed_password": "$2b$12$...",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }

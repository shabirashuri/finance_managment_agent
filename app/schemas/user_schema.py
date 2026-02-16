from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePassword123"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str  # Can be username or email
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "SecurePassword123"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (excludes password)."""
    user_id: str
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "johndoe",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00"
            }
        }


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "username": "johndoe",
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00"
                }
            }
        }


class TokenData(BaseModel):
    """Schema for decoded token payload."""
    user_id: Optional[str] = None

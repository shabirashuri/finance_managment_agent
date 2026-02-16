from datetime import datetime
from typing import Optional
import logging
from app.core.database import users_collection
from app.core.auth import get_password_hash, verify_password
from app.core.exceptions import UserAlreadyExistsError, AuthenticationError
from app.models.user import UserModel
from app.schemas.user_schema import UserRegister

logger = logging.getLogger(__name__)


async def create_user(user_data: UserRegister) -> UserModel:
    """
    Create a new user account.
    
    Args:
        user_data: User registration data
        
    Returns:
        Created user model
        
    Raises:
        UserAlreadyExistsError: If email or username already exists
    """
    # Check if email already exists
    existing_email = await users_collection.find_one({"email": user_data.email})
    if existing_email:
        raise UserAlreadyExistsError("email")
    
    # Check if username already exists
    existing_username = await users_collection.find_one({"username": user_data.username})
    if existing_username:
        raise UserAlreadyExistsError("username")
    
    # Create user model
    user = UserModel(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password)
    )
    
    # Insert into database
    await users_collection.insert_one(user.model_dump())
    
    logger.info(f"Created new user: {user.username} ({user.email})")
    
    return user


async def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user with username/email and password.
    
    Args:
        username: Username or email
        password: Plain text password
        
    Returns:
        User document if authentication successful, None otherwise
        
    Raises:
        AuthenticationError: If credentials are invalid
    """
    # Try to find user by username or email
    user = await users_collection.find_one({
        "$or": [
            {"username": username},
            {"email": username}
        ]
    })
    
    if not user:
        raise AuthenticationError("Invalid username or password")
    
    # Verify password
    if not verify_password(password, user["hashed_password"]):
        raise AuthenticationError("Invalid username or password")
    
    # Check if user is active
    if not user.get("is_active", True):
        raise AuthenticationError("Account is inactive")
    
    logger.info(f"User authenticated: {user['username']}")
    
    return user


async def get_user_by_email(email: str) -> Optional[dict]:
    """
    Get user by email.
    
    Args:
        email: User email
        
    Returns:
        User document or None
    """
    return await users_collection.find_one({"email": email})


async def get_user_by_id(user_id: str) -> Optional[dict]:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        User document or None
    """
    return await users_collection.find_one({"user_id": user_id})


async def get_user_by_username(username: str) -> Optional[dict]:
    """
    Get user by username.
    
    Args:
        username: Username
        
    Returns:
        User document or None
    """
    return await users_collection.find_one({"username": username})

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
import logging
from app.schemas.user_schema import UserRegister, UserLogin, Token, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.core.auth import create_access_token, get_current_user
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user account.
    
    Args:
        user_data: User registration data (email, username, password)
        
    Returns:
        JWT token and user information
    """
    try:
        # Create user
        user = await create_user(user_data)
        
        # Generate JWT token
        access_token = create_access_token(
            data={"sub": user.user_id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Prepare user response
        user_response = UserResponse(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with username/email and password.
    
    Args:
        credentials: Login credentials (username/email, password)
        
    Returns:
        JWT token and user information
    """
    try:
        # Authenticate user
        user = await authenticate_user(credentials.username, credentials.password)
        
        # Generate JWT token
        access_token = create_access_token(
            data={"sub": user["user_id"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Prepare user response
        user_response = UserResponse(
            user_id=user["user_id"],
            email=user["email"],
            username=user["username"],
            is_active=user.get("is_active", True),
            created_at=user["created_at"]
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to login"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        User information
    """
    return UserResponse(
        user_id=current_user["user_id"],
        email=current_user["email"],
        username=current_user["username"],
        is_active=current_user.get("is_active", True),
        created_at=current_user["created_at"]
    )

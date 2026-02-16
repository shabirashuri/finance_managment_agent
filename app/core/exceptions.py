from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class AuthorizationError(HTTPException):
    """Raised when user doesn't have permission."""
    def __init__(self, detail: str = "Not authorized to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class SessionNotFoundError(HTTPException):
    """Raised when session doesn't exist."""
    def __init__(self, session_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session_id} not found"
        )


class SessionValidationError(HTTPException):
    """Raised when session constraints are violated."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class UserAlreadyExistsError(HTTPException):
    """Raised when trying to register with existing email/username."""
    def __init__(self, field: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with this {field} already exists"
        )

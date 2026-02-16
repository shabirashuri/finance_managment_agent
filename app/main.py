from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth_router import router as auth_router
from app.api.session_router import router as session_router
from app.api.document_router import router as document_router
from app.api.full_tally import router as tally_router
from app.core.logging_config import logger

# Initialize logging
logger.info("Starting AI Cheque Tally System")

app = FastAPI(
    title="AI Cheque Tally System",
    description="Production-ready financial reconciliation system with JWT authentication",
    version="2.0.0"
)

# Include routers
app.include_router(auth_router)
app.include_router(session_router)
app.include_router(tally_router)
app.include_router(document_router)  # Keep for backward compatibility

# CORS configuration
origins = [
    "http://localhost:5173",   # Vite default
    "http://127.0.0.1:5173",   # sometimes browser uses this
    "http://localhost:3000",   # React default
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Cheque Tally System",
        "version": "2.0.0"
    }


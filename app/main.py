from fastapi import FastAPI
from app.api.document_router import router as document_router
from app.api.full_tally import router as tally_router

app = FastAPI(title="AI Cheque Tally System")

app.include_router(document_router)
app.include_router(tally_router)


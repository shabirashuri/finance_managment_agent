from fastapi import FastAPI
from app.api.document_router import router as document_router
from app.api.full_tally import router as tally_router


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Cheque Tally System")

app.include_router(document_router)
app.include_router(tally_router)



origins = [
    "http://localhost:5173",   # Vite default
    "http://127.0.0.1:5173",   # sometimes browser uses this
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # allowed frontend origins
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

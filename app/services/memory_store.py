import uuid
from typing import Dict, Any

# Separate storage for each document type
company_documents: Dict[str, Dict[str, Any]] = {}
bank_documents: Dict[str, Dict[str, Any]] = {}


def store_company_document(text: str, file_path: str) -> str:
    document_id = str(uuid.uuid4())

    company_documents[document_id] = {
        "file_path": file_path,
        "raw_text": text,
        "status": "uploaded_and_extracted",
        "type": "company"
    }

    return document_id


def store_bank_document(text: str, file_path: str) -> str:
    document_id = str(uuid.uuid4())

    bank_documents[document_id] = {
        "file_path": file_path,
        "raw_text": text,
        "status": "uploaded_and_extracted",
        "type": "bank"
    }

    return document_id


def get_company_document(document_id: str):
    return company_documents.get(document_id)


def get_bank_document(document_id: str):
    return bank_documents.get(document_id)

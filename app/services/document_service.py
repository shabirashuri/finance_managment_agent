from app.core.database import documents_collection
from app.models.document_model import DocumentModel
from datetime import datetime


async def create_document(document_type: str, raw_text: str):
    document = DocumentModel(
        document_type=document_type,
        raw_text=raw_text
    )

    await documents_collection.insert_one(document.dict())
    return document.document_id


async def get_document(document_id: str):
    return await documents_collection.find_one(
        {"document_id": document_id}
    )


async def update_document(document_id: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()

    await documents_collection.update_one(
        {"document_id": document_id},
        {"$set": update_data}
    )

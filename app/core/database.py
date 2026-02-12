
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

documents_collection = database["documents"]


from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]

# Collections
users_collection = database["users"]
sessions_collection = database["sessions"]
documents_collection = database["documents"]

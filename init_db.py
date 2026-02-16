"""
Database initialization script.
Run this once to create indexes for optimal performance.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URL, DATABASE_NAME


async def create_indexes():
    """Create database indexes for all collections."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]
    
    print("Creating indexes...")
    
    # Users collection indexes
    await db.users.create_index("user_id", unique=True)
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    print("✓ Created users indexes")
    
    # Sessions collection indexes
    await db.sessions.create_index("session_id", unique=True)
    await db.sessions.create_index("user_id")
    await db.sessions.create_index([("user_id", 1), ("created_at", -1)])
    print("✓ Created sessions indexes")
    
    # Documents collection indexes
    await db.documents.create_index("document_id", unique=True)
    await db.documents.create_index("session_id")
    await db.documents.create_index("user_id")
    print("✓ Created documents indexes")
    
    print("\n✅ All indexes created successfully!")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(create_indexes())

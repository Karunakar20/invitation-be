from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

# MongoDB client
client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_url)

# Database
db: AsyncIOMotorDatabase = client[settings.mongodb_name]


async def get_mongodb():
    """Dependency to get MongoDB database instance"""
    return db


async def close_mongodb():
    """Close MongoDB connection"""
    client.close()
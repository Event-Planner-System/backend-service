from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings


client = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    print("✅ Connected to MongoDB")


async def close_mongo_connection():
    global client
    client.close()
    print("❌ Disconnected from MongoDB")
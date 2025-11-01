from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# Use Motor for async MongoDB operations
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
users_collection = db["users"]

async def connect_to_mongo():
    """Test MongoDB connection"""
    try:
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

async def close_mongo_connection():
    """Close MongoDB connection"""
    client.close()
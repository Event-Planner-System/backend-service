from database.connection import users_collection
from fastapi import HTTPException

class UserRepository:
    @staticmethod
    async def get_user_by_username(username: str) -> dict | None:
        user = await users_collection.find_one({"username": username})
        return user  # Return None if not found, don't raise exception
    
    @staticmethod
    async def get_user_by_email(email: str) -> dict | None:
        user = await users_collection.find_one({"email": email})
        return user  # Return None if not found, don't raise exception
    
    @staticmethod
    async def save_user(user: dict) -> dict:
        result = await users_collection.insert_one(user)
        user["_id"] = result.inserted_id
        return user
    
    @staticmethod
    async def delete_user(username: str) -> bool:
        result = await users_collection.delete_one({"username": username})
        if result.deleted_count == 0:
            raise ValueError(f"User with username '{username}' not found")
        return True
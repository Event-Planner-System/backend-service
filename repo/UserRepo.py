from model.UserModel import UserModel
import pymongo

class UserRepo:
    def __init__(self, collection):
        self.collection = collection

    async def get_user_by_username(self, username: str) -> dict:
        user = await self.collection.find_one({"username": username})
        if not user:
            raise ValueError(f"User with username '{username}' not found")
        return user

    async def get_user_by_email(self, email: str) -> dict:
        user = await self.collection.find_one({"email": email})
        if not user:
            raise ValueError(f"User with email '{email}' not found")
        return user

    async def save_user(self, user: dict) -> dict:
        try:
            result = await self.collection.insert_one(user)
            user["_id"] = result.inserted_id
        
        except pymongo.errors.DuplicateKeyError:
            raise ValueError(f"Username '{user['username']}' already exists")
        return user

    async def delete_user(self, username: str) -> bool:
        result = await self.collection.delete_one({"username": username})
        if result.deleted_count == 0:
            raise ValueError(f"User with username '{username}' not found")
        return True
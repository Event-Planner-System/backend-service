from fastapi import APIRouter, Depends, HTTPException, status
from ..database.connection import db


router = APIRouter(prefix="/user", tags=["User"])

@router.get("/getuser")
async def get_user(username: str):
    try:
        user = await db["users"].find_one({"username": username})
        return user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    
@router.delete("/deleteuser")
async def delete_user(username: str):
    try:
        result = await db["users"].delete_one({"username": username})
        return {"deleted": result}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    
# @router.put("/updateuser", response_model=UserDTO)
# async def update_user(user: UserDTO):
#     try:
#         existing_user = await user_repo.get_user_by_username(user.username)
#         updated_user = existing_user.copy()
#         updated_user.update(user.dict(exclude_unset=True))
#         await user_repo.collection.replace_one({"username": user.username}, updated_user)
#         return updated_user
#     except ValueError as ve:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
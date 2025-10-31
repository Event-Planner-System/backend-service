from fastapi import APIRouter, Depends, HTTPException, status
from model.UserDTO import UserDTO
from repo.UserRepo import UserRepo

router = APIRouter(prefix="/user", tags=["User"])
user_repo= UserRepo()

@router.get("/getuser", response_model=UserDTO)
async def get_user(username: str):
    try:
        user = await user_repo.get_user_by_username(username)
        return user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    
@router.delete("/deleteuser")
async def delete_user(username: str):
    try:
        result = await user_repo.delete_user(username)
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
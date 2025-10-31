from fastapi import APIRouter, Depends, HTTPException, status
from model.UserDTO import UserDTO
from service.AuthService import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/register", response_model=UserDTO)
async def register_user(user: UserDTO):
    try:
        new_user = await auth_service.register_user(user)
        return new_user
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
@router.post("/login")
async def login_user(username: str, password: str):
    try:
        token = await auth_service.login_user(username, password)
        return {"access_token": token}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ve))
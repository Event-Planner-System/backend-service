from fastapi import APIRouter
from model.user import User
from service.AuthService import register_user, login_user


router = APIRouter()


@router.post("/register")
async def register(user: User):
    return await register_user(user)


@router.get("/login")
async def login(user: User):
    return await login_user(user.email, user.password)


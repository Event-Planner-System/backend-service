from model.user import User
from fastapi import APIRouter, HTTPException, status
from service.AuthService import register_user, login_user


router = APIRouter()

#register endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User):
    try:
        result = await register_user(user)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#login endpoint
@router.post("/login")
async def login_endpoint(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        token = await login_user(email, password)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

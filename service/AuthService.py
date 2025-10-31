from core.security import hash_password, verify_password, verify_password, create_access_token
from model.user import User
from fastapi import HTTPException
from repo.UserRepo import UserRepository
from datetime import timedelta
from service.EmailService import EmailService
from email_templates.RegisterationTemplate import RegistrationTemplate


async def register_user(user : User):
    existing_email = await UserRepository.get_user_by_email(user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered, Login instead.")
    exisiting_username = await UserRepository.get_user_by_username(user.userName)
    if exisiting_username:
        raise HTTPException(status_code=400, detail="Username already taken, choose another one.")
    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    saved_user = await UserRepository.save_user(user_dict)
    
    # Send registration email
    template = RegistrationTemplate()
    email_service = EmailService(template)
    context = {"name": user.userName, "app_name": "Event planner"}
    email_service.send_email(user.email, context)
    
    return {"message": "User registered successfully"}


    

async def login_user(email: str, password: str):
    user = await UserRepository.get_by_email(email)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create token payload
    token_data = {"sub": user["email"]}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=60))

    return {"access_token": access_token,}
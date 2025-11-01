from ..core.security import hash_password, verify_password, create_access_token
from ..model.user import User
from fastapi import HTTPException
from datetime import timedelta
from ..email_templates.RegisterationTemplate import RegistrationTemplate
from ..service.EmailService import EmailService
from ..database import connection

async def register_user(user: User):
    # Check if email already exists
    db = connection.db
    existing_email = await db["users"].find_one({"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    existing_username = await db["users"].find_one({"username": user.username})
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken, please choose another one")
    
    # Hash password and save user
    hashed_password = hash_password(user.password)
    user_dict = user.model_dump()  
    user_dict["password"] = hashed_password
    
    await db["users"].insert_one(user_dict)
    
    
    # Send registration email
    template = RegistrationTemplate()
    email_service = EmailService(template)
    context = {"name": user.username, "app_name": "Event planner"}
    email_service.send_email(user.email, context)
    
    return {"message": "User registered successfully"}




async def login_user(email: str, password: str):
    db = connection.db
    # Get user from database
    user = await db["users"].find_one({"email": email})
    
    # Check if user exists and password is correct
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create token payload
    token_data = {"sub": user["email"], "username": user["username"]}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=60))
    
    return {"access_token": access_token, "token_type": "bearer"}
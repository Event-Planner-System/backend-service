from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    username: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=72)
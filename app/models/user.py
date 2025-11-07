from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    username: Optional[str] = Field(None, min_length=5, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=72)
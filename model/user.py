from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    userName: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(...,
                           pattern=r"^[^\s]{8,}$",
                           description="Password must contain uppercase, lowercase, number, and special character (no spaces)"
                        )

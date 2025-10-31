from fastapi import FastAPI
from api.AuthAPI import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from model.user import User
from service.AuthService import register_user


app = FastAPI(
    title="User Management API",
    description="FastAPI + MongoDB example with authentication",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(auth_router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "User Management Service is running."}

@app.get("/test-connection")
async def test_connection():
    return {"status": "success", "message": "Frontend connected successfully!"}

@app.post("/register")
async def register(user: User):
    return await register_user(user)

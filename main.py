
from fastapi import FastAPI
from api.AuthAPI import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from database.connection import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - runs when server starts
    await connect_to_mongo()
    yield
    # Shutdown - runs when server stops
    await close_mongo_connection()

app = FastAPI(
    title="User Management API",
    description="FastAPI + MongoDB example with authentication",
    version="1.0.0",
    lifespan=lifespan  # 👈 Add this
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "User Management Service is running."}

@app.get("/test-connection")
async def test_connection():
    return {"status": "success", "message": "Frontend connected successfully!"}
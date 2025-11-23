from fastapi import FastAPI
from .routes.auth_routes import router as auth_router
from .routes.event_routes import router as event_router  # Add this line
from fastapi.middleware.cors import CORSMiddleware
from .database.connection import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown: Close MongoDB connection
    await close_mongo_connection()


app = FastAPI(
    title="Event Planner APIs",
    lifespan=lifespan
)


# CORS configuration
origins = [
    "http://localhost:3000",  # frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(event_router, prefix="/events", tags=["Events"])  # Add this line


@app.get("/")
async def root():
    return {"message": "Event Planner is running."}


@app.get("/test-connection", tags=["Connection Test For Frontend"])
async def test_connection():
    return {"status": "success", "message": "Frontend connected successfully!"}
# from fastapi import FastAPI
# from .routes.auth_routes import router as auth_router
# from .routes.event_routes import router as event_router  # Add this line
# from fastapi.middleware.cors import CORSMiddleware
# from .database.connection import connect_to_mongo, close_mongo_connection
# from contextlib import asynccontextmanager
# from .routes.invitation_routes import router as invitation_router
# from .routes.search_routes import router as search_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup: Connect to MongoDB
#     await connect_to_mongo()
#     yield
#     # Shutdown: Close MongoDB connection
#     await close_mongo_connection()


# app = FastAPI(
#     title="Event Planner APIs",
#     lifespan=lifespan
# )


# # CORS configuration
# origins = [
#     "http://localhost:3000",  # frontend URL
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(event_router, prefix="/events", tags=["Events"])
# app.include_router(invitation_router, prefix="/invitations", tags=["Invitations"])
# app.include_router(search_router, prefix="/events", tags=["Search"])


# @app.get("/")
# async def root():
#     return {"message": "Event Planner is running.",}


# @app.get("/test-connection", tags=["Connection Test For Frontend"])
# async def test_connection():
#     return {"status": "success", "message": "Frontend connected successfully!"}



from fastapi import FastAPI
from .routes.auth_routes import router as auth_router
from .routes.event_routes import router as event_router
from fastapi.middleware.cors import CORSMiddleware
from .database.connection import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager
from .routes.invitation_routes import router as invitation_router
from .routes.search_routes import router as search_router
import os


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


# CORS configuration - UPDATED FOR PRODUCTION
# Read from environment variable or use default for local development
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")

# Convert comma-separated string to list
origins = [origin.strip() for origin in allowed_origins.split(",")]

print(f"🔧 CORS enabled for origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Now supports multiple origins from env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(event_router, prefix="/events", tags=["Events"])
app.include_router(invitation_router, prefix="/invitations", tags=["Invitations"])
app.include_router(search_router, prefix="/events", tags=["Search"])


@app.get("/")
async def root():
    return {"message": "Event Planner is running."}


@app.get("/test-connection", tags=["Connection Test For Frontend"])
async def test_connection():
    return {"status": "success", "message": "Frontend connected successfully!"}
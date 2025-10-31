from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "user_management_db"
    
    SECRET_KEY: str = "JWT_SecretKey_For_UserManagementService"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

settings = Settings()


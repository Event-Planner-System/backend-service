from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    MONGO_URI: str 
    DB_NAME: str 
    
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    EMAIL_ADDRESS : str
    EMAIL_APP_KEY : str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()



import os
import secrets
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# Generate a secure secret key
secret_key = secrets.token_hex(32) 

class Settings(BaseModel):
    MONGO_DETAILS: str = "mongodb://localhost:27017"
    JWT_SECRET_KEY: str = secret_key
    JWT_ALGORITHM: str = "HS256"

settings = Settings()
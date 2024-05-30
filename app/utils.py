from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional

from .schema import SignIn
from .database import db_instance
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(password:str):
    return pwd_context.hash(password)
  
  
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
  
  
  
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db, email: str):
    user = await db["users"].find_one({"email": email})
    if user:
        return SignIn(email=user['email'], password=user['password'])



async def authenticate_user(db, email: str, password: str):
    user = await get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
  

async def get_current_user(request: Request):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  api_key = request.headers.get("Authorization")
  if not api_key:
      raise credentials_exception

  token = api_key.split("Bearer ")[-1] 
  try:
      payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options={"verify_signature": False})
      email: str = payload.get("sub")
      if email is None:
          raise credentials_exception
  except JWTError:
        raise credentials_exception
  user = await get_user(db_instance, email=email)
  if user is None:
      raise credentials_exception
  return user
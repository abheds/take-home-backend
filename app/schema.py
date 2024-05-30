
from pydantic import BaseModel

class CreateUser(BaseModel):
  email: str
  password: str
  full_name: str 
  
  
class AuthUser(BaseModel):
  email: str
  fullname: str 
  
class SignIn(BaseModel):
  email: str
  password: str
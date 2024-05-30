from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: str
    fullname: str
    password: str
    

class Job(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str
    company_name: str
    company_description: str
    company_url: str
    post_url: str
    post_apply:str
    minimum_companset: float
    maximum_companset: float
    job_type: str
    role_type: str
    education: str
    original_post: str
    work_location_type: str 
    city: str
    region: str
    country: str 
    published_at: datetime 
    updated_at: datetime


def ResponseModel(data=dict, message:str = '', status_code:int = 200):
    response = {
      "status_code" : status_code,
      "message": message
    }
    if data is not None:
      response.update({"data":data})
    return response


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
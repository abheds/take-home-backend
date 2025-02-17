from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fuzzywuzzy import process
from datetime import timedelta

from .models import User
from .schema import CreateUser, SignIn
from .utils import hash_pass, authenticate_user, create_access_token, get_current_user
from .database import db_instance

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login",)
async def login_user(form_data: SignIn = Depends()):
    user = await authenticate_user(db_instance, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    data = {
      "access_token": access_token, 
      "token_type": "bearer",
      "email":user.email
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@app.post('/createUser', status_code=status.HTTP_201_CREATED)
async def create_users(user:CreateUser,):
    hashed_password = hash_pass(user.password)
    user_dict = user.dict()
    user_dict.update({"password": hashed_password})
    try:
        await db_instance["users"].insert_one(user_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail="User already exists")
      
    return JSONResponse(
      status_code=status.HTTP_201_CREATED,
      content={"message":"User Created Successfully!"}
    )
    
@app.post('/job_search', status_code=status.HTTP_200_OK)
async def job_search(job_title:str, current_user: User = Depends(get_current_user)):
  jobs = await db_instance["jobs"].find().to_list(length=None)
  if job_title is not None:
    
    filtered_jobs = [job['job_name'] for job in jobs]
    jobs = process.extract(job_title, filtered_jobs, limit=1)
    match_result = [title for title, score in jobs]
    jobs = await db_instance["jobs"].find({"job_name": {"$in": match_result}}).to_list(length=None)
  for job in jobs:
        job['_id'] = str(job['_id'])
        
  return JSONResponse(
    content={
      "data":jobs
    },
    status_code=status.HTTP_200_OK
  )
  

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Job Posting API"}

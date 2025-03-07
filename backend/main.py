from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.userdata import *
import os
from typing import Optional
from dotenv import load_dotenv 
load_dotenv()
MONGO_URI= os.getenv("MONGO_URI")
class UserBody(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username:str
    password:str
app = FastAPI()

@app.get('/')
def home():
    return "We made it"


@app.post("/auth/login",tags=["Authentication"])
def login(user:UserBody):
    user ={"username":user.username,"password":user.password}
    print(user)
    user_id,username= login_user(db_uri=MONGO_URI,db_name="crayonics",collection_name="users",document=user)
    
    if user_id != False:
        return {"user_id":user_id,"message":f"welcome back {username}"}
    return JSONResponse(status_code=401,content="Invalid login details")


@app.post("/auth/signup",tags=["Authentication"])
def signUp(user:UserBody):
    user ={"username":user.username,"password":user.password,"first_name":user.firstName,"last_name":user.lastName}
    user_id= create_user(db_uri=MONGO_URI,db_name="crayonics",collection_name="users",document=user)
    if user_id != False:
        return {"user_id":user_id,"message":"User created Successfully"}
    return JSONResponse(status_code=status.HTTP_226_IM_USED,content="user already Exists")

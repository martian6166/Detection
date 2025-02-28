from fastapi import FastAPI
from pydantic import BaseModel

class user(BaseModel):
    username:str
    password:str
app = FastAPI()

@app.get('/')
def home():
    return "We made it"


@app.post('/auth/login')
def login(user:user):
    pass

@app.post('/auth/register')
def register(user:user):
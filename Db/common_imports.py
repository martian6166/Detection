from dotenv import load_dotenv
import os
from v2.users import insert_user,fetch_users
import redis
import json


load_dotenv()

DB_NAME = os.getenv('POSTGRES_DB_NAME')
USER= os.getenv('POSTGRES_USERNAME')
PASSWORD= os.getenv('POSTGRES_PASSWORD')
HOST = os.getenv('POSTGRES_HOST')
PORT= os.getenv('POSTGRES_PORT')
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USERNAME =os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
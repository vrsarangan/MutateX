import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

def get_db():
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)
    db = client["mutatex"]  # use your DB name here
    return db

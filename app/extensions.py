from app.logcontrol import logger
from flask_pymongo import PyMongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

conn = os.getenv("MONGO_URI")

client = MongoClient(conn)
db = client.get_database("data")
logs_db = db.get_collection("webhook")
logger("Database").info("Database created")

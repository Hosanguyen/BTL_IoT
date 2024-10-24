from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv('DB_NAME')

url = "mongodb+srv://nguyenthienhoa:12345@cluster0.jujotvv.mongodb.net/IOT?retryWrites=true&w=majority&appName=Cluster0"

connection = MongoClient(url)
db = connection[db_name]


def getConnection():
    return connection


def getDb():
    return db

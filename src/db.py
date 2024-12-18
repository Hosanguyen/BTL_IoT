from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv('MONGO_DB')

url = os.getenv('MONGO_URI')

connection = MongoClient(url)
db = connection[db_name]
print(url)

def getConnection():
    return connection


def getDb():
    return db

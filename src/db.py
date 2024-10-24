from pymongo import MongoClient

url = "mongodb+srv://nguyenthienhoa:12345@cluster0.jujotvv.mongodb.net/IOT?retryWrites=true&w=majority&appName=Cluster0"

connection = MongoClient(url)

def getConnection():
    return connection
# from src.db import getDb
# from src.model.FireAlarm import FireAlarm
from db import getDb
from model.FireAlarm import FireAlarm

db = getDb()
collection = db['FireAlarm']
print("Connected to FireAlarm database")

def getFireAlarmData():
    return collection.find({})

def save_FireAlarm(firealarm: FireAlarm):
    collection.insert_one(firealarm.get_info())








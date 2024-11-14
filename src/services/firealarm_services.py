# from src.db import getDb
# from src.model.FireAlarm import FireAlarm
from db import getDb
from model.FireAlarm import FireAlarm
from bson import json_util
import json

db = getDb()
collection = db['FireAlarm_Log']
print("Connected to FireAlarm database")

def getFireAlarmData():
    data = list(collection.find({}))
    return json.loads(json_util.dumps(data))

def save_FireAlarm(firealarm: FireAlarm):
    collection.insert_one(firealarm.get_info())








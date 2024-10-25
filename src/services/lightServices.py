from db import getDb
import datetime

db = getDb()
collection = db["ControlLight"]

def updateLightState(device, status):
    timestamp = datetime.datetime.now()
    data = {
        'device': device,
        'status': status,
        'timestamp': timestamp
    }
    collection.insert_one(data)

def getLightState(device):
    data = collection.find_one({'device': device}, sort=[('timestamp', -1)])
    if data:
        data['_id'] = str(data['_id'])
    return data

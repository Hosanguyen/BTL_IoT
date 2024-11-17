from db import getDb
import datetime
from model.Led import Led
from services.deviceService import updateState
import json

db = getDb()
collection = db["ControlLight"]

def updateLightState(led):
    collection.insert_one(led.toSchema())
    updateState(led)
    # updateMode(Led)

def getLightState(deviceId):
    data = collection.find_one({'deviceId': deviceId}, sort=[('timestamp', -1)])
    led = Led(data['deviceId'], data['status'], data['timestamp'])
    return led

def getLog(deviceId):
    query = {"deviceId": deviceId}
    devices = list(collection.find(query).sort("timestamp", -1).limit(5)) 
    return json.loads(json.dumps(devices, default=str))

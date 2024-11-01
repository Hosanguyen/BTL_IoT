from db import getDb
import datetime
from model.Led import Led

db = getDb()
collection = db["ControlLight"]

def updateLightState(led):
    collection.insert_one(led.toSchema())

def getLightState(device):
    data = collection.find_one({'device': device}, sort=[('timestamp', -1)])
    led = Led(data['name'], data['status'], data['timestamp'])
    return led

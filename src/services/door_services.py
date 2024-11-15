# from src.db import getDb
from db import getDb
import unittest
import datetime

# from src.model.Door import Door
# from src.services.mqtt_services import getMqttClient
from model.Door import Door
from services.mqtt_services import getMqttClient

db = getDb()
collection_log = db['Door_Log']
collection_device = db['Device']
topic_door = 'home/door'
mqtt_client = getMqttClient()

def control_door(door: Door):
    mqtt_client.publish(topic_door, door.deviceId+";"+door.status)
    save_door_status(door)


def save_door_status(door: Door):
    timestamp = datetime.datetime.now()
    door.timestamp = timestamp
    data = door.get_info()
    collection_device.update_one(
        {'deviceId': door.deviceId},  # Tìm thiết bị theo name
        {'$set': {'status': door.status}}  # Cập nhật trường status
    )
    collection_log.insert_one(data)


def get_door_status(device_id):
    data = collection_device.find_one({'deviceId': device_id})
    return data


# def get_door_alive(deviceId):
#     data = collection_device.find_one({'device': deviceId})
#     return data['is_live']
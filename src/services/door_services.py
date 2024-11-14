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


# class Test(unittest.TestCase):
#     def test(self):
#         self.assertEqual(getDb(), db)
#         self.assertEqual(collection_log, db['Door_Log'])

#     def test_function(self):
#         # door = Door('door', 'OPEN', datetime.datetime.now())
#         # save_door_status(door)
#         # data = get_door_status('door')
#         # self.assertEqual(data['name'], 'door')
#         # self.assertEqual(data['status'], 'OPEN')
#         # self.assertEqual(data['timestamp'], data['timestamp'])

#         door = Door('door', 'CLOSE', datetime.datetime.now())
#         save_door_status(door)
#         data = get_door_status('door')
#         self.assertEqual(data['name'], 'door')
#         self.assertEqual(data['status'], 'CLOSE')
#         self.assertEqual(data['timestamp'], data['timestamp'])

#     def test_set_door_alive(self):
#         set_door_alive(1)
#         data = collection_device.find_one({'device': 'door'})
#         self.assertEqual(data['is_live'], 1)

#         set_door_alive(0)
#         data = collection_device.find_one({'device': 'door'})
#         self.assertEqual(data['is_live'], 0)


def control_door(door: Door):
    mqtt_client.publish(topic_door, door.deviceId+";"+door.status)
    save_door_status(door)



def save_door_status(door: Door):
    timestamp = datetime.datetime.now()
    door.timestamp = timestamp
    mqtt_client.publish(topic_door, door.status)
    data = door.get_info()
    collection_device.update_one(
        {'deviceId': door.deviceId},  # Tìm thiết bị theo name
        {'$set': {'status': door.status}}  # Cập nhật trường status
    )
    collection_log.insert_one(data)


def get_door_status(device_id):
    print(device_id)
    data = collection_device.find_one({'deviceId': device_id})
    return data


# def get_door_alive(deviceId):
#     data = collection_device.find_one({'device': deviceId})
#     return data['is_live']

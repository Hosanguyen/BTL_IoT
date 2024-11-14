# from src.db import getDb
from db import getDb
import unittest
import datetime

# from src.model.Door import Door
# from src.services.mqtt_services import getMqttClient
from model.Door import Door
from services.mqtt_services import getMqttClient

db = getDb()
collection = db['log_status']
collection_device = db['Device']
topic_door = 'home/door'
mqtt_client = getMqttClient()


class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(getDb(), db)
        self.assertEqual(collection, db['log_status'])

    def test_function(self):
        # door = Door('door', 'OPEN', datetime.datetime.now())
        # save_door_status(door)
        # data = get_door_status('door')
        # self.assertEqual(data['name'], 'door')
        # self.assertEqual(data['status'], 'OPEN')
        # self.assertEqual(data['timestamp'], data['timestamp'])

        door = Door('door', 'CLOSE', datetime.datetime.now())
        save_door_status(door)
        data = get_door_status('door')
        self.assertEqual(data['name'], 'door')
        self.assertEqual(data['status'], 'CLOSE')
        self.assertEqual(data['timestamp'], data['timestamp'])

    def test_set_door_alive(self):
        set_door_alive(1)
        data = collection_device.find_one({'device': 'door'})
        self.assertEqual(data['is_live'], 1)

        set_door_alive(0)
        data = collection_device.find_one({'device': 'door'})
        self.assertEqual(data['is_live'], 0)


def control_door(door: Door):
    mqtt_client.publish(topic_door, door.status)
    save_door_status(door)


def save_door_status(door: Door):
    timestamp = datetime.datetime.now()
    door.timestamp = timestamp
    data = door.get_info()
    collection.insert_one(data)


def get_door_status(device):
    data = collection.find_one({'name': device}, sort=[('timestamp', -1)])
    if data:
        data.pop('_id')
    else:
        data = {'status': 'Door is empty'}
    return data


def set_door_alive(is_live):
    try:
        collection_device.update_one({'device': 'door'}, {'$set': {'is_live': is_live}})
    except:
        collection_device.insert_one({'device': 'door', 'is_live': is_live})

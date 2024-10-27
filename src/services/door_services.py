from src.db import getDb
import unittest
import datetime

from src.model.Door import Door

db = getDb()
collection = db['log_status']

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(getDb(), db)
        self.assertEqual(collection, db['log_status'])

    def test_function(self):
        save_door_status('door', 'OPEN')
        data = get_door_status('door')
        self.assertEqual(data['device'], 'door')
        self.assertEqual(data['status'], 'OPEN')
        self.assertEqual(data['timestamp'], data['timestamp'])

        save_door_status('door', 'CLOSE')
        data = get_door_status('door')
        self.assertEqual(data['device'], 'door')
        self.assertEqual(data['status'], 'CLOSE')
        self.assertEqual(data['timestamp'], data['timestamp'])


def save_door_status(door: Door):
    timestamp = datetime.datetime.now()
    door.timestamp = timestamp
    data = door.get_info()
    collection.insert_one(data)


def get_door_status(device):
    data = collection.find_one({'device': device}, sort=[('timestamp', -1)])
    return data


from src.db import getDb

import datetime

db = getDb()
collection = db.log_status


def save_door_status(device, status):
    timestamp = datetime.datetime.now()
    data = {
        'device': device,
        'status': status,
        'timestamp': timestamp
    }
    db[collection].insert_one(data)


def get_door_status(device):
    data = db[collection].find_one({'device': device}, sort=[('timestamp', -1)])
    return data

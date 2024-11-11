from db import getDb
from model.Device import Device
from bson import ObjectId

db = getDb()

collection = db['device']

def getListDevice(device_type):
    devices = collection.find({'type': device_type})
    
    # Chuyển đổi các ObjectId thành chuỗi và trả về danh sách thiết bị
    return [{**device, "_id": str(device["_id"])} for device in devices]

def addDevice(device):
    collection.insert_one(device.toSchema())

def deleteDevice(device_id):
    return collection.delete_one({'_id': ObjectId(device_id)})

def updateState(device):
    collection.update_one(
        {'deviceId': device.deviceId},  # Tìm thiết bị theo name
        {'$set': {'status': device.status}}  # Cập nhật trường status
    )

def updateMode(deviceId, mode):
    collection.update_one(
        {'deviceId': deviceId},  # Tìm thiết bị theo name
        {'$set': {'mode': mode}}  # Cập nhật trường mode
    )
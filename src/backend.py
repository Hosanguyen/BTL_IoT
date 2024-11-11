from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from flask_cors import CORS
from dotenv import load_dotenv
from Module.SmartDoor import smart_door
from Module.FireAlarm import fire_alarm
from Module.ControlLight import ControlLight
from flask_socketio import SocketIO
from services.mqtt_services import init_socket
from services.deviceService import getListDevice, addDevice, deleteDevice
from model.Device import Device
from Module.DeviceAPI import DeviceAPI
import os
from model.FireAlarm import FireAlarm
from services.firealarm_services import save_FireAlarm
import json

# Load từ file .env
load_dotenv()

# Tạo ứng dụng Flask
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

# Register the relay Blueprint
app.register_blueprint(smart_door)
app.register_blueprint(fire_alarm)
app.register_blueprint(ControlLight)
app.register_blueprint(DeviceAPI)

CORS(app)


init_socket(socketio)

if __name__ == '__main__':
    HOST = os.getenv('HOST')
    HOST_PORT = int(os.getenv('HOST_PORT'))
    app.run(host=HOST, port=HOST_PORT)

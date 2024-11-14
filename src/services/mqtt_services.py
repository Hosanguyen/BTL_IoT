import json

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
# from src.db import getDb
# from src.model.FireAlarm import FireAlarm
# from src.services.firealarm_services import save_FireAlarm
from db import getDb
from model.FireAlarm import FireAlarm
from services.firealarm_services import save_FireAlarm
from model.Led import Led
from services.lightServices import updateLightState
from services.deviceService import updateState, updateAlive
import datetime, time
import threading
load_dotenv()

BROKER = os.getenv('BROKER_URL')
PORT = int(os.getenv('BROKER_PORT'))

preLogLed = time.time()
preDoor = time.time()
prePump = time.time()

mqtt_client = mqtt.Client()
def init_socket(socketio):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # thêm các topic cần subscribe ở đây
        client.subscribe("home/door")
        client.subscribe("home/firealarm")
        client.subscribe("home/light")

    def on_message(client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f'{topic} {payload}')
        cur = time.time()
        # xử lý message ở đây
        if msg.topic == 'home/firealarm':
            global prePump
            prePump = cur
            updateAlive("pump", True)
            socketio.emit('pump', 'True')
            print('Fire alarm: ', msg.payload.decode())
            # ghi log vào database
            [deviceId, status, pump_status] = payload.split(";")
            fire_alarm = FireAlarm(deviceId, status, pump_status)
            save_FireAlarm(fire_alarm)
            # Phát sự kiện qua SocketIO
            socketio.emit('firealarm', payload)
        if(topic == 'home/light'):
            # Gửi thông điệp qua mqtt dạng name;status ví dụ "Led1;ON"
            global preLogLed
          
            [deviceId, action] = payload.split(";")
            if(action == 'LOGON'):
                updateAlive("Led", True)
                socketio.emit('log', 'True')
                preLogLed = cur
                led = Led(deviceId, "ON", datetime.datetime.now())
                updateLightState(led)
                log = led.toSchema()
                log['timestamp'] = log['timestamp'].isoformat()
                socketio.emit('status_logs', [log])
            elif (action == 'LOGOFF'):
                updateAlive("Led", True)
                socketio.emit('log', 'True')
                preLogLed = cur
                led = Led(deviceId, "OFF", datetime.datetime.now())
                updateLightState(led)
                log = led.toSchema()
                log['timestamp'] = log['timestamp'].isoformat()
                socketio.emit('status_logs', [log])
            elif (action == 'ON' or action == 'OFF'):
                led = Led(deviceId, action, datetime.datetime.now())
                updateLightState(led)
                updateState(led)
                # Phát sự kiện qua SocketIO
                socketio.emit('light', payload)
            

    #Kết nối tới broker
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    print("Connected to broker")
    def check_timeout():
        global preLogLed
        global preDoor
        global prePump
        while True:
            time.sleep(1)  # Check every 1 seconds
            cur = time.time()
            if cur - preLogLed > 10:
                updateAlive("Led", False)
                socketio.emit('log', 'False')
            if cur - preDoor > 10:
                updateAlive("Door", False)
                socketio.emit('door', 'False')
            if cur - prePump > 10:
                updateAlive("pump", False)
                socketio.emit('pump', 'False')

    # Run the timeout check in a separate thread
    threading.Thread(target=check_timeout, daemon=True).start()


def getMqttClient():
    return mqtt_client

#
# import unittest
#
# class Test(unittest.TestCase):
#     def test(self):
#         self.assertEqual(getMqttClient(), mqtt_client)
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
import datetime

load_dotenv()

BROKER = os.getenv('BROKER_URL')
PORT = int(os.getenv('BROKER_PORT'))


mqtt_client = mqtt.Client()
def init_socket(socketio):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # thêm các topic cần subscribe ở đây
        client.subscribe("home/firealarm")
        client.subscribe("home/light")

    def on_message(client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f'{topic} {payload}')
        # xử lý message ở đây
        if msg.topic == 'home/firealarm':
            print('Fire alarm: ', msg.payload.decode())
            # ghi log vào database
            data = json.load(msg.payload.decode())
            fire_alarm = FireAlarm(sensor_status=data.get('sensor_status',False), pump_status=data.get('pump_status',False), siren_status=data.get('siren_status',False))
            save_FireAlarm(fire_alarm)
        if(topic == 'home/light'):
            # Gửi thông điệp qua mqtt dạng name;status ví dụ "Light1;ON"
            [device, action] = payload.split(";")
            led = Led(device, action, datetime.datetime.now())
            updateLightState(led)

            # Phát sự kiện qua SocketIO
            socketio.emit('light', payload)

    #Kết nối tới broker
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    print("Connected to broker")

def getMqttClient():
    return mqtt_client

#
# import unittest
#
# class Test(unittest.TestCase):
#     def test(self):
#         self.assertEqual(getMqttClient(), mqtt_client)
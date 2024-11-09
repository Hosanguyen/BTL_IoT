import json

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
from src.db import getDb
from src.model.FireAlarm import FireAlarm
from src.services.firealarm_services import save_FireAlarm

load_dotenv()

BROKER = os.getenv('BROKER_URL')
PORT = int(os.getenv('BROKER_PORT'))


mqtt_client = mqtt.Client()
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # thêm các topic cần subscribe ở đây
    client.subscribe("home/firealarm")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # xử lý message ở đây
    if msg.topic == 'home/firealarm':
        print('Fire alarm: ', msg.payload.decode())
    #     # ghi log vào database
        data = json.loads(msg.payload.decode())
        print('Fire alarm:', data)
    #     fire_alarm = FireAlarm(sensor_status=data.get('sensor_status',False), pump_status=data.get('pump_status',False), siren_status=data.get('siren_status',False))
    #     save_FireAlarm(fire_alarm)


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
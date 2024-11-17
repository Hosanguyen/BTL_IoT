import paho.mqtt.client as mqtt
import time
from dotenv import load_dotenv
import os

load_dotenv()

BROKER = os.getenv('BROKER_URL')
PORT = int(os.getenv('BROKER_PORT'))

client = mqtt.Client()  
status = "OFF"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("home/pump")

def on_message(client, userdata, msg):
    global status
    if msg.topic == "home/pump":
        print("Status", msg.payload.decode())
        status = msg.payload.decode()

client.on_connect = on_connect
client.on_message = on_message 

client.connect(BROKER, PORT, 60)
client.loop_start()

dem=0
while True:
    time.sleep(1)
    print("Publishing message..." + str(dem))
    print(f"FireAlarm;YES;{status}")
    # print("FireAlarm;YES;OFF")
    client.publish("home/firealarm", f"FireAlarm;YES;{status}")
    dem+=1
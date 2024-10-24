import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

BROKER = os.getenv('BROKER')
PORT = int(os.getenv('BROKER_PORT'))

mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, PORT, 60)


def getMqttClient():
    return mqtt_client

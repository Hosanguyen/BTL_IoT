from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from flask_cors import CORS
from dotenv import load_dotenv
from Module.SmartDoor import smart_door
from Module.FireAlarm import fire_alarm
import os
from model.FireAlarm import FireAlarm
from services.firealarm_services import save_FireAlarm
import json

# Load từ file .env
load_dotenv()

# Tạo ứng dụng Flask
app = Flask(__name__)

# Register the relay Blueprint
app.register_blueprint(smart_door)
app.register_blueprint(fire_alarm)

CORS(app)

# Thông tin MQTT broker
BROKER = os.getenv('BROKER_URL')
PORT = int(os.getenv('BROKER_PORT'))

TOPIC_RELAY1 = "home/relay1"
TOPIC_RELAY2 = "home/relay2"

# Tạo MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, PORT, 60)


# Route API để điều khiển relay 1
@app.route('/api/relay1', methods=['POST'])
def control_relay1():
    data = request.json
    action = data.get('action')
    if action == 'ON':
        mqtt_client.publish(TOPIC_RELAY1, 'ON')
        return jsonify({'status': 'Relay 1 Bật'}), 200
    elif action == 'OFF':
        mqtt_client.publish(TOPIC_RELAY1, 'OFF')
        return jsonify({'status': 'Relay 1 Tắt'}), 200
    else:
        return jsonify({'error': 'Hành động không hợp lệ'}), 400


# Route API để điều khiển relay 2
@app.route('/api/relay2', methods=['POST'])
def control_relay2():
    data = request.json
    action = data.get('action')
    if action == 'ON':
        mqtt_client.publish(TOPIC_RELAY2, 'ON')
        return jsonify({'status': 'Relay 2 Bật'}), 200
    elif action == 'OFF':
        mqtt_client.publish(TOPIC_RELAY2, 'OFF')
        return jsonify({'status': 'Relay 2 Tắt'}), 200
    else:
        return jsonify({'error': 'Hành động không hợp lệ'}), 400
mqtt_client.loop_start()
if __name__ == '__main__':
    HOST = os.getenv('HOST')
    HOST_PORT = int(os.getenv('HOST_PORT'))
    app.run(host=HOST, port=HOST_PORT)

from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from flask_cors import CORS

# Tạo ứng dụng Flask
app = Flask(__name__)

CORS(app)

# Thông tin MQTT broker
BROKER = "192.168.1.109"
PORT = 1883
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import request, session, Blueprint, jsonify
from services.mqtt_services import mqtt_client

ControlLight = Blueprint("ControlLight", __name__)

TOPIC_RELAY1 = "home/relay1"
TOPIC_RELAY2 = "home/relay2"

# Route API để điều khiển relay 1
@ControlLight.route('/api/relay1', methods=['POST'])
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
@ControlLight.route('/api/relay2', methods=['POST'])
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


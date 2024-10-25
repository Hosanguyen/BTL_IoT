from flask import request, session, Blueprint, jsonify
from services.mqtt_services import mqtt_client
from services.lightServices import updateLightState, getLightState

ControlLight = Blueprint("ControlLight", __name__)

TOPIC_RELAY1 = "home/relay1"
TOPIC_RELAY2 = "home/relay2"

TOPIC_AUTO_RELAY1 = "auto/relay1"
TOPIC_AUTO_RELAY2 = "auto/relay2"

# Lắng nghe từ các topic auto/relay1 và auto/relay2
auto_relay1_state = None
auto_relay2_state = None

# Hàm callback khi có tin nhắn đến từ MQTT
def on_message(client, userdata, msg):
    global auto_relay1_state, auto_relay2_state
    topic = msg.topic
    payload = msg.payload.decode()
    print(topic + " " + payload)
    if topic == TOPIC_AUTO_RELAY1:
        auto_relay1_state = payload
        updateLightState("Light1", payload)  # Cập nhật trạng thái cho Light1
    elif topic == TOPIC_AUTO_RELAY2:
        auto_relay2_state = payload
        updateLightState("Light2", payload)  # Cập nhật trạng thái cho Light2

# Đăng ký callback cho MQTT client
mqtt_client.on_message = on_message

# Subscribe các topic auto/relay1 và auto/relay2
mqtt_client.subscribe(TOPIC_AUTO_RELAY1)
mqtt_client.subscribe(TOPIC_AUTO_RELAY2)
mqtt_client.loop_start()

# Route API để điều khiển relay 1
@ControlLight.route('/api/relay1', methods=['POST'])
def control_relay1():
    data = request.json
    action = data.get('action')
    updateLightState("Light1", action)
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
    updateLightState("Light2", action)
    if action == 'ON':
        mqtt_client.publish(TOPIC_RELAY2, 'ON')
        return jsonify({'status': 'Relay 2 Bật'}), 200
    elif action == 'OFF':
        mqtt_client.publish(TOPIC_RELAY2, 'OFF')
        return jsonify({'status': 'Relay 2 Tắt'}), 200
    else:
        return jsonify({'error': 'Hành động không hợp lệ'}), 400

# Endpoint auto/light1 để lấy trạng thái từ MongoDB
@ControlLight.route('/auto/light1', methods=['GET'])
def get_auto_light1():
    light1_state = getLightState("Light1")
    if light1_state:
        return jsonify(light1_state), 200
    else:
        return jsonify({'error': 'No data available for Auto Light 1'}), 404

# Endpoint auto/light2 để lấy trạng thái từ MongoDB
@ControlLight.route('/auto/light2', methods=['GET'])
def get_auto_light2():
    light2_state = getLightState("Light2")
    if light2_state:
        return jsonify(light2_state), 200
    else:
        return jsonify({'error': 'No data available for Auto Light 2'}), 404

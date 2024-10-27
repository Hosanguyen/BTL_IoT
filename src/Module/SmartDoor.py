from flask import Blueprint, request, jsonify

from src.model.Door import Door
from src.services.door_services import save_door_status
from src.services.mqtt_services import getMqttClient





mqtt_client = getMqttClient()
smart_door = Blueprint('smart_door', __name__)
topic_door = 'home/door'


@smart_door.route('/api/door', methods=['POST'])
def control_door():
    data = request.json
    action = data.get('action')
    if action == 'OPEN':
        mqtt_client.publish(topic_door, 'OPEN')
        return jsonify({'status': 'Door open'}), 200
    elif action == 'CLOSE':
        mqtt_client.publish(topic_door, 'CLOSE')
        return jsonify({'status': 'Door close'}), 200
    else:
        return jsonify({'error': 'Action invalid'}), 400


@smart_door.route('/api/camera_door', methods=['POST'])
def camera_door_open():
    data = request.json
    action = data.get('action')
    namedoor = data.get('door_name')

    door = Door(namedoor, 'OPEN', None, True)
    if action == 'OPEN':
        mqtt_client.publish(topic_door, 'OPEN')
        save_door_status(door)
        return jsonify({'status': 'Door open'}), 200

    else:
        return jsonify({'error': 'Action invalid'}), 400




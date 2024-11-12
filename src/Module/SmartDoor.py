from flask import Blueprint, request, jsonify

# from src.model.Door import Door
# from src.services.door_services import save_door_status, get_door_status
# from src.services.mqtt_services import getMqttClient
from model.Door import Door
from services.door_services import save_door_status, get_door_status
from services.mqtt_services import getMqttClient

mqtt_client = getMqttClient()
smart_door = Blueprint('smart_door', __name__)
topic_door = 'home/door'


@smart_door.route('/api/door', methods=['GET'])
def check_door_status():
    req = request.json
    device = req.get('door_name')
    data = get_door_status(device)
    stt = data['status']
    print(stt)
    if stt == 'OPEN':
        return jsonify({'status': 'OPEN'}), 200
    elif stt == 'CLOSE':
        return jsonify({'status': 'CLOSE'}), 200
    elif stt == 'Door is empty':
        return jsonify({'status': 'Door is empty'}), 300
    else:
        return jsonify({'error': 'Door not found'}), 404


@smart_door.route('/api/door', methods=['POST'])
def control_door():
    data = request.json
    action = data.get('action')
    namedoor = data.get('door_name')

    door = Door(namedoor, action, None)
    if 'OPEN' in action:
        save_door_status(door)
        return jsonify({'status': 'Door open'}), 200
    elif action == 'CLOSE':
        save_door_status(door)
        return jsonify({'status': 'Door close'}), 200
    else:
        return jsonify({'error': 'Action invalid'}), 400


@smart_door.route('/api/camera_door', methods=['POST'])
def camera_door_open():
    data = request.json
    namedoor = data.get('door_name')

    door = Door(namedoor, 'OPEN', None, True)
    if door.status == 'OPEN':
        save_door_status(door)
        return jsonify({'status': 'Door open'}), 200

    else:
        return jsonify({'error': 'Action invalid'}), 400

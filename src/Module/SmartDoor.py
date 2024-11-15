from flask import Blueprint, request, jsonify

# from src.model.Door import Door
# from src.services.door_services import save_door_status, get_door_status
# from src.services.mqtt_services import getMqttClient
from model.Door import Door
from services.door_services import control_door, get_door_status
from services.mqtt_services import getMqttClient
from services.recognition_services import RecognitionService
from db import getDb
mqtt_client = getMqttClient()
smart_door = Blueprint('smart_door', __name__)
topic_door = 'home/door'

# Thêm biến để lưu trữ socketio instance
socketio = None
database = getDb()
recognition_service = RecognitionService(database=database)

def init_door_socket(socket):
    global socketio
    socketio = socket


@smart_door.route('/api/door', methods=['GET'])
def check_door_status():
    deviceId = request.args.get('door_id')
    data = get_door_status(deviceId)
    print("in check door status" + data)
    if not data:
        return jsonify({'status': 'Door not found'}), 300
    if data['alive'] == 1:
        stt = data['status']
        if stt == 'OPEN':
            return jsonify({'status': 'OPEN'}), 200
        elif stt == 'CLOSE':
            return jsonify({'status': 'CLOSE'}), 200
        elif stt == 'Door not found':
            return jsonify({'status': 'Door not found'}), 300
        else:
            return jsonify({'error': 'Not alive'}), 404
    else:
        return jsonify({'error': 'Not alive'}), 404


@smart_door.route('/api/door', methods=['POST'])
def dieukhien_door():
    data = request.json
    action = data.get('action')
    namedoor = data.get('door_id')
    data_status = get_door_status(namedoor)
    if not data or data_status['alive'] == 0:
        print("in dieukhien_door" + namedoor)
        return jsonify({'status': 'Door not found'}), 300

    door = Door(namedoor, action, None)
    if 'OPEN' in action:
        control_door(door)
        return jsonify({'status': 'Door open'}), 200
    elif action == 'CLOSE':
        control_door(door)
        return jsonify({'status': 'Door close'}), 200
    elif action == 'STOP':
        control_door(door)
        return jsonify({'status': 'Door stop'}), 200
    else:
        return jsonify({'error': 'Action invalid'}), 400

@smart_door.route('/api/camera_door', methods=['POST'])
def camera_door_open():
    try:
        data = request.json
        namedoor = data.get('door_id')
        user_id = data.get('user_id')
        image_data = data.get('image')  # Nhận base64 image từ client AI
        
        # Kiểm tra trạng thái cửa
        door_data = get_door_status(namedoor)
        if not door_data or door_data['alive'] == 0:
            return jsonify({'status': 'Door not found'}), 300

        # Lưu thông tin nhận diện và lấy record với URL
        recognition_record = recognition_service.save_recognition(namedoor, image_data, user_id)
        
        # Gửi thông tin nhận diện tới frontend qua socket.io
        if socketio:
            socketio.emit('door_recognition', recognition_record)

        # Mở cửa
        door = Door(namedoor, 'OPEN', None, True)
        control_door(door)
        return jsonify({
            'status': 'Door open',
            'recognition': recognition_record
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@smart_door.route('/api/recognitions', methods=['GET'])
def get_recognitions():
    try:
        door_id = request.args.get('door_id')
        limit = int(request.args.get('limit', 10))
        records = recognition_service.get_recognitions(door_id, limit)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@smart_door.route('/api/recognitions/<recognition_id>', methods=['GET'])
def get_recognition(recognition_id):
    try:
        record = recognition_service.get_recognition_by_id(recognition_id)
        if record:
            return jsonify(record), 200
        return jsonify({'error': 'Recognition not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
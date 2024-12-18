from flask import Blueprint, request, jsonify
# from src.services.firealarm_services import getFireAlarmData
# from src.services.mqtt_services import getMqttClient
from services.firealarm_services import getFireAlarmData
from services.mqtt_services import getMqttClient
from services.deviceService import updateState
from model.Device import Device

mqtt_client = getMqttClient()
fire_alarm = Blueprint('fire_alarm', __name__)

@fire_alarm.route('/api/getFireAlarm', methods=['GET'])
def getFireAlarm():
    # page = request.args.get('page','Guest')
    try:
        return jsonify({'message': 'Nhận thành công', 'data': getFireAlarmData()}), 200
    except:
        return jsonify({'message': 'Lỗi không xác định'}), 500

@fire_alarm.route('/api/firealarm/pump', methods=['POST'])
def control_pump():
    data = request.json
    action = data.get('status')
    type = data.get('type')
    idDevice = data.get('idDevice')
    device = Device(idDevice, None, None, None, action , type)
    if action == 'ON':
        updateState(device)
        mqtt_client.publish('home/pump', 'ON')
        return jsonify({'status': 'Bơm bật'}), 200
    elif action == 'OFF':
        updateState(device)
        mqtt_client.publish('home/pump', 'OFF')
        return jsonify({'status': 'Bơm tắt'}), 200
    else:
        return jsonify({'error': 'Hành động không hợp lệ'}), 400





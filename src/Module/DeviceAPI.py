from flask import request, session, Blueprint, jsonify
from services.mqtt_services import mqtt_client
from model.Device import Device
from services.deviceService import getListDevice, addDevice, deleteDevice

DeviceAPI = Blueprint("DeviceAPI", __name__)


@DeviceAPI.route('/api/device', methods=['GET'])
def getDevice():
    device_type = request.args.get('type')
    return jsonify({'listDevice':getListDevice(device_type)})

@DeviceAPI.route('/api/register/device', methods=['POST'])
def register_device():
    data = request.json
    deviceId = data.get('device')
    type = data.get('type')
    topic =""
    if(type == 'Led'):
        topic = 'home/light'
    status = 'OFF'
    mode = 'manual'
    device = Device(deviceId, topic, True, mode, status, type)
    addDevice(device)
    return jsonify({'status': f'Thiết bị {deviceId} đã được đăng ký'}), 200

@DeviceAPI.route('/api/delete/device', methods=['DELETE'])
def delete_device():
    data = request.json
    device_id = data.get('id')
    if device_id:
        result = deleteDevice(device_id)
        if result.deleted_count > 0:
            return jsonify({'status': 'Thiết bị đã được xóa'}), 200
        else:
            return jsonify({'error': 'Không tìm thấy thiết bị'}), 404
    else:
        return jsonify({'error': 'Thiếu ID thiết bị'}), 400
from flask import request, session, Blueprint, jsonify
from services.mqtt_services import mqtt_client
from services.lightServices import updateLightState, getLightState
from services.deviceService import getListDevice, updateMode
from model.Led import Led
import datetime

ControlLight = Blueprint("ControlLight", __name__)

topic = "home/light"

# Route API để điều khiển led
@ControlLight.route('/api/light', methods=['POST'])
def control():
    data = request.json
    mes = data.get('message')
    device = mes.split(";")[0]
    action = mes.split(";")[1]

    led = Led(device, action, datetime.datetime.now())
    updateLightState(led)
    if action == 'ON':
        mqtt_client.publish(topic, mes)
        return jsonify({'status': f'{device} Bật'}), 200
    elif action == 'OFF':
        mqtt_client.publish(topic, mes)
        return jsonify({'status': f'{device} Tắt'}), 200
    else:
        return jsonify({'error': 'Hành động không hợp lệ'}), 400

@ControlLight.route('/api/light/auto', methods = ['POST'])
def auto():
    data = request.json
    mes = data.get('message')
    [deviceId, mode] = mes.split(";")
    updateMode(deviceId, mode)
    led = Led(deviceId, "OFF", datetime.datetime.now())
    mqtt_client.publish('home/light', deviceId + ";OFF")
    updateLightState(led)
    mqtt_client.publish(topic, mes)
    return jsonify({'status': 'success'}), 200


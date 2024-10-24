from flask import Blueprint, request, jsonify
from src.services.mqtt_services import getMqttClient

mqtt_client = getMqttClient()
smart_door = Blueprint('smart_door', __name__)
topic_door = 'home/door'

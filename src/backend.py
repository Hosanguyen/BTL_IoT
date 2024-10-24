from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from flask_cors import CORS
from dotenv import load_dotenv
import os
from Module.ControlLight import ControlLight
# Load từ file .env
load_dotenv()

# Tạo ứng dụng Flask
app = Flask(__name__)

CORS(app)

app.register_blueprint(ControlLight)

if __name__ == '__main__':
    HOST = os.getenv('HOST')
    HOST_PORT = int(os.getenv('HOST_PORT'))
    app.run(host=HOST, port=HOST_PORT)

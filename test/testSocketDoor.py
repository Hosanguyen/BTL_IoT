from socketio import Client
import time
import logging

class DoorSocketClient:
    def __init__(self, server_url='http://localhost:5000'):
        self.sio = Client(reconnection=True, reconnection_delay=5)
        self.server_url = server_url
        self.is_connected = False
        
        # Thiết lập logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Đăng ký các event handlers
        @self.sio.on('connect')
        def on_connect():
            self.is_connected = True
            self.logger.info('Connected to server')
            
        @self.sio.on('disconnect')
        def on_disconnect():
            self.is_connected = False
            self.logger.info('Disconnected from server')
            self.attempt_reconnect()
            
        @self.sio.on('connect_error')
        def on_connect_error():
            self.is_connected = False
            self.logger.error('Connection failed')
            self.attempt_reconnect()
            
        @self.sio.on('door')
        def on_door(data):
            # data format: "deviceId;action"
            device_id, action = data.split(';')
            self.logger.info(f'Door event received - Device: {device_id}, Action: {action}')
            
        @self.sio.on('dooralive')
        def on_door_alive(status):
            self.logger.info(f'Door alive status: {status}')
            
    def attempt_reconnect(self):
        """Thực hiện reconnect sau mỗi 5 giây"""
        if not self.is_connected:
            self.logger.info('Attempting to reconnect in 5 seconds...')
            time.sleep(5)
            try:
                if not self.is_connected:
                    self.connect()
            except Exception as e:
                self.logger.error(f'Reconnection failed: {e}')
            
    def connect(self):
        """Kết nối đến server"""
        try:
            self.logger.info(f'Attempting to connect to {self.server_url}')
            self.sio.connect(self.server_url)
        except Exception as e:
            self.logger.error(f'Connection failed: {e}')
            self.attempt_reconnect()
            
    def disconnect(self):
        """Ngắt kết nối"""
        self.sio.disconnect()
        
    def wait(self):
        """Giữ client chạy và lắng nghe các events"""
        while True:
            if not self.is_connected:
                self.attempt_reconnect()
            time.sleep(1)

if __name__ == "__main__":
    # Khởi tạo và chạy client
    client = DoorSocketClient()
    try:
        client.connect()
        client.wait()
    except KeyboardInterrupt:
        print("\nShutting down client...")
        client.disconnect()
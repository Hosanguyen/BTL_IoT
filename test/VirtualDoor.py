import paho.mqtt.client as mqtt
import time

class DoorStatus:
    LOGOPEN = "LOGOPEN"
    LOGCLOSE = "LOGCLOSE"
    LOGOPENING = "LOGOPENING"
    LOGCLOSING = "LOGCLOSING"

class DoorAction:
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    STOP = "STOP"

class SmartDoor:
    def __init__(self):
        # Khởi tạo các biến trạng thái
        self.device_id = "Main door"
        self.status = DoorStatus.LOGCLOSE
        self.position = 0  # 0: đóng hoàn toàn, 10: mở hoàn toàn
        self.is_moving = False
        self.current_action = None
        
        # Biến để theo dõi thời gian publish
        self.last_publish_time = 0
        
        # Biến để theo dõi thời gian cho quá trình mở/đóng
        self.movement_start_time = 0
        
        # Thiết lập MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Kết nối tới MQTT broker
        self.client.connect("localhost", 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("home/door")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"Received message: {message}")
        
        # Phân tích tin nhắn theo định dạng "device_id;action"
        try:
            device_id, action = message.split(';')
            if device_id == self.device_id:  # Chỉ xử lý tin nhắn cho đúng thiết bị
                if action == DoorAction.OPEN:
                    self.current_action = DoorAction.OPEN
                elif action == DoorAction.CLOSE:
                    self.current_action = DoorAction.CLOSE
                elif action == DoorAction.STOP:
                    self.current_action = DoorAction.STOP
        except ValueError:
            print(f"Invalid message format: {message}")

    def publish_status(self):
        """Publish status if 5 seconds have passed since last publish"""
        current_time = time.time()
        if current_time - self.last_publish_time >= 5:
            message = f"{self.device_id};{self.status}"
            self.client.publish("home/door", message)
            print(f"Status published: {message}")
            self.last_publish_time = current_time

    def handle_open(self):
        if self.position < 10:
            print("Starting opening process...")
            self.is_moving = True
            self.position += 1
            self.current_action = DoorAction.OPEN
            self.status = DoorStatus.LOGOPENING
            self.movement_start_time = time.time()
            if self.position % 5 == 0:
                self.client.publish("home/door", f"{self.device_id};{DoorStatus.LOGOPENING}")
            # self.client.publish("home/door", f"{self.device_id};{DoorStatus.LOGOPENING}")
            print(f"Door is opening... Position: {self.position}")
            print(f"Current status: {self.status}")
            print(f"Current action in handle_open: {self.current_action}")
        else:
            self.current_action = None
            self.status = DoorStatus.LOGOPEN
            self.client.publish("home/door", f"{self.device_id};{DoorStatus.LOGOPEN}")
            print("Door is already fully opened")

    def handle_close(self):
        if self.position > 0:
            print("Starting closing process...")
            self.is_moving = True
            self.position -= 1
            self.current_action = DoorAction.CLOSE
            self.status = DoorStatus.LOGCLOSING
            self.movement_start_time = time.time()
            if self.position % 5 == 0:
                self.client.publish("home/door", f"{self.device_id};{DoorStatus.LOGCLOSING}")
            print(f"Door is closing... Position: {self.position}")
        else:
            self.current_action = None
            self.status = DoorStatus.LOGCLOSE
            self.client.publish("home/door", f"{self.device_id};{DoorStatus.LOGCLOSE}")
            print("Door is already fully closed")

    def handle_stop(self):
        if self.is_moving:
            print("Handling stop command...")
            self.is_moving = False
            # Update status based on current position
            self.current_action = None
            if self.position > 0:
                self.status = DoorStatus.LOGOPEN
                self.client.publish("home/door", f"{self.device_id};{DoorStatus.LOGOPEN}")
            else:
                self.status = DoorStatus.LOGCLOSE
                self.client.publish("home/door", f"{self.device_id};{DoorStatus.LOGCLOSE}")

    # def update_position(self):
    #     """Update door position based on elapsed time"""
    #     if self.is_moving:
    #         elapsed_time = time.time() - self.movement_start_time
    #         steps = int(elapsed_time)  # Mỗi bước mất 1s
            
    #         if self.current_action == DoorAction.OPEN:
    #             target_position = min(10, self.position + steps)
    #             if target_position != self.position:
    #                 self.position = target_position
    #                 print(f"Opening... Position: {self.position}")
    #                 if self.position >= 10:
    #                     self.is_moving = False
    #                     self.status = DoorStatus.LOGOPEN
    #                     print("Door fully opened")
            
    #         elif self.current_action == DoorAction.CLOSE:
    #             target_position = max(0, self.position - steps)
    #             if target_position != self.position:
    #                 self.position = target_position
    #                 print(f"Closing... Position: {self.position}")
    #                 if self.position <= 0:
    #                     self.is_moving = False
    #                     self.status = DoorStatus.LOGCLOSE
    #                     print("Door fully closed")
            
    #         if steps > 0:
    #             self.movement_start_time = time.time()

    def run(self):
        """Main loop của chương trình"""
        self.client.loop_start()
        print("Door system started...")
        
        try:
            while True:
                # Cập nhật vị trí cửa
                if self.current_action in [DoorAction.OPEN, DoorAction.CLOSE]:
                    self.is_moving = True
                print(f"Current position: {self.position}")
                print(f"Current status: {self.status}")
                print(f"Current action: {self.current_action}")
                if self.current_action == DoorAction.OPEN:
                    print("1")
                    self.handle_open()
                elif self.current_action == DoorAction.CLOSE:
                    print("2")
                    self.handle_close()
                elif self.current_action == DoorAction.STOP:
                    print("3")
                    self.handle_stop()
                
                # Publish status nếu đã đủ 5s
                self.publish_status()
                
                # Delay nhỏ để giảm tải CPU
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("Stopping the door system...")
            self.client.loop_stop()

if __name__ == "__main__":
    door = SmartDoor()
    door.run()
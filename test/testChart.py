import paho.mqtt.client as mqtt
import time
import random

# Thông tin kết nối MQTT
broker = "localhost"  # Thay đổi broker nếu cần
port = 1883
topic = "home/light"  # Thay đổi topic nếu cần

# Hàm khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    print("Kết nối MQTT thành công với mã trả về: " + str(rc))

# Khởi tạo client MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Kết nối đến broker
client.connect(broker, port, 60)

# Giả lập gửi dữ liệu mỗi 5 giây
try:
    client.loop_start()  # Bắt đầu vòng lặp nền của MQTT
    while True:
        # Tạo trạng thái ngẫu nhiên cho từng đèn
        led1_status = random.choice(["LOGON", "LOGOFF"])
        led2_status = random.choice(["LOGON", "LOGOFF"])
        
        # Tạo tin nhắn theo định dạng "Led1;LOGON" hoặc "Led2;LOGOFF"
        payload_led1 = f"Led1;{led1_status}"
        payload_led2 = f"Led2;{led2_status}"
        
        # Gửi dữ liệu của từng đèn lên topic
        client.publish(topic, payload_led1)
        print(f"Đã gửi: {payload_led1}")
        
        # Chờ 5 giây trước khi gửi dữ liệu tiếp
        time.sleep(5)
        
        client.publish(topic, payload_led2)
        print(f"Đã gửi: {payload_led2}")
        
        # Chờ 5 giây trước khi gửi dữ liệu tiếp
        time.sleep(5)

except KeyboardInterrupt:
    print("Dừng chương trình.")
finally:
    client.loop_stop()  # Dừng vòng lặp nền của MQTT
    client.disconnect()  # Ngắt kết nối MQTT

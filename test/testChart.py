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
        # Giả lập dữ liệu ngẫu nhiên
        data1 = "Led1;LOGON"
        data2 = "Led1;LOGOFF"
        data3 = "Led2;LOGON"
        data4 = "Led2;LOGOFF"
        
        # Chuyển đổi dữ liệu sang chuỗi JSON
        payload = str(data1)
        
        # Gửi dữ liệu lên topic
        client.publish(topic, payload)
        print(f"Đã gửi: {payload}")
        
        # Chờ 5 giây trước khi gửi dữ liệu tiếp
        time.sleep(5)
        payload = str(data2)
        
        # Gửi dữ liệu lên topic
        client.publish(topic, payload)
        print(f"Đã gửi: {payload}")
        
        # Chờ 5 giây trước khi gửi dữ liệu tiếp
        time.sleep(5)
        payload = str(data3)
        
        # Gửi dữ liệu lên topic
        client.publish(topic, payload)
        print(f"Đã gửi: {payload}")
        
        # Chờ 5 giây trước khi gửi dữ liệu tiếp
        time.sleep(5)
        payload = str(data4)
        
        # Gửi dữ liệu lên topic
        client.publish(topic, payload)
        print(f"Đã gửi: {payload}")
        
        # Chờ 5 giây trước khi gửi dữ liệu tiếp
        time.sleep(5)

except KeyboardInterrupt:
    print("Dừng chương trình.")
finally:
    client.loop_stop()  # Dừng vòng lặp nền của MQTT
    client.disconnect()  # Ngắt kết nối MQTT

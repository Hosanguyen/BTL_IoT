#include <WiFi.h>
#include <PubSubClient.h>

// Thông tin kết nối WiFi
// const char* ssid = "P 501 87 Yen Xa";
// const char* password = "0984999668p";
// const char* mqtt_server = "192.168.51.103";
const char* ssid = "ADMIN 3116";
const char* password = "88888888";
const char* mqtt_server = "192.168.137.148";
// Thông tin kết nối WiFi
// const char* ssid = "nv.minh_";
// const char* password = "1234567890";
// const char* mqtt_server = "172.20.10.10";

WiFiClient espClient;
PubSubClient client(espClient);

// Khai báo các chân điều khiển L298N
#define IN1 18  // Chân IN1 trên L298N
#define IN2 19  // Chân IN2 trên L298N
#define ENA 22

int speed = 25;
int position = 10;  // Biến vị trí toàn cục (0 - cửa đóng hoàn toàn, 10 - cửa mở hoàn toàn)
unsigned long lastPrintTime = 0;
unsigned long lastPublishTime = 0; 
unsigned long lastPublishTime2 = 0; // Biến để theo dõi thời gian publish tin nhắn
bool isOpening = false;
bool isClosing = false;
bool moveToHalf = false; // Biến xác định nếu đang di chuyển đến vị trí giữa

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  analogWrite(ENA,0);
}

void setup_wifi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  String command = "";
  for (int i = 0; i < length; i++) {
    command += (char)payload[i];
  }

  if (String(topic) == "home/door") {
    int separatorIndex = command.indexOf(';');
    String deviceId = command.substring(0, separatorIndex);
    String action = command.substring(separatorIndex + 1);

    if (deviceId == "Main door") {
      if (action == "OPEN") {
        openDoor();
      } else if (action == "OPEN12") {
        moveDoorToHalf();
      } else if (action == "CLOSE") {
        closeDoor();
      } else if (action == "STOP") {
        stopDoor();
      }
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("home/door");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if ((isOpening || isClosing || moveToHalf) && millis() - lastPrintTime >= 1000) {
    lastPrintTime = millis();
    
    // Cập nhật vị trí cửa mỗi giây
    if (isOpening && position > 0) {
      position--;
      Serial.print("Opening, Position: ");
    } else if (isClosing && position < 10) {
      position++;
      Serial.print("Closing, Position: ");
    } else if (moveToHalf) {
      if (position > 5) {
        position--;
        Serial.print("Moving to half (closing), Position: ");
      } else if (position < 5) {
        position++;
        Serial.print("Moving to half (opening), Position: ");
      }
    }
    Serial.println(position);

    // Nếu đang di chuyển đến vị trí giữa và đạt đến 5, dừng lại
    if (moveToHalf && position == 5) {
      stopDoor();
      moveToHalf = false;  // Reset lại trạng thái sau khi đã đến giữa
    }

    // Dừng khi đạt giới hạn (0 hoặc 10)
    if (position == 0 || position == 10) {
      stopDoor();
    }
  }

  // Publish tin nhắn mỗi 5 giây
  if (millis() - lastPublishTime >= 5000 && !isOpening && !isClosing) {
    lastPublishTime = millis();
    if (position == 0) {
      client.publish("home/door", "Main door;LOGOPEN");
    } else if (position == 10) {
      client.publish("home/door", "Main door;LOGCLOSE");
    } else {
      client.publish("home/door", "Main door;LOGSTOP");
    }

  }
  if (millis() - lastPublishTime2 >= 1000) {
    lastPublishTime2 = millis();
    if (isOpening) {
      client.publish("home/door", "Main door;LOGOPENING");
    } else if (isClosing) {
      client.publish("home/door", "Main door;LOGCLOSING");
    }
  }
}

void openDoor() {
  if (position > 0) {  // Nếu cửa chưa mở hoàn toàn
    isOpening = true;
    isClosing = false;
    moveToHalf = false;  // Không dừng ở vị trí giữa nếu không sử dụng lệnh MOVE_HALF
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, speed);
    Serial.println("Opening door...");
  } else {
    Serial.println("Door is already fully open.");
  }
}

void closeDoor() {
  if (position < 10) {  // Nếu cửa chưa đóng hoàn toàn
    isClosing = true;
    isOpening = false;
    moveToHalf = false;  // Không dừng ở vị trí giữa nếu không sử dụng lệnh MOVE_HALF
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, speed);
    Serial.println("Closing door...");
  } else {
    Serial.println("Door is already fully closed.");
  }
}

void moveDoorToHalf() {
  if (position > 5) {  // Nếu vị trí hiện tại lớn hơn 5, cần đóng để đến vị trí 5
    isClosing = false;
    isOpening = false;
    moveToHalf = true;
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA, speed);
    Serial.println("Moving door to half (closing)...");
  } else if (position < 5) {  // Nếu vị trí hiện tại nhỏ hơn 5, cần mở để đến vị trí 5
    isClosing = false;
    isOpening = false;
    moveToHalf = true;
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, speed);
    Serial.println("Moving door to half (opening)...");
  } else {
    Serial.println("Door is already at half position.");
  }
}

void stopDoor() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);
  Serial.println("Stopping door...");

  isOpening = false;
  isClosing = false;
  moveToHalf = false;
}

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Thông tin kết nối WiFi
const char* ssid = "NTH";
const char* password = "hoanguyen";

// Thông tin MQTT Broker
const char* mqtt_server = "192.168.110.81";
const int mqtt_port = 1883;

const int ledpin1 = 19;
const int ledpin2 = 21;
const int lightSensorPin = 32;  // Chân cảm biến ánh sáng
#define FLAME_SENSOR_PIN 5  // Pin for flame sensor
#define RELAY_PIN 4         // Pin for relay controlling the light
#define RELAY_PIN2 18 

const char* topicLed = "home/light"; 
const char* mqtt_pub_topic = "home/firealarm";
const char* mqtt_sub_topic = "home/pump";
int pump_status = 1;

WiFiClient espClient;
PubSubClient client(espClient);

bool light1Status = false;  // Trạng thái đèn hiện tại
bool light2Status = false;
bool lightStatus = false;   // Biến để theo dõi trạng thái ánh sáng
bool autoMode = false;      // Biến để theo dõi chế độ tự động
bool autoMode2 = false;

const long delayLog = 5000; // Gửi log mỗi 5 giây
unsigned long previousLog = 0;

// Hàm kết nối WiFi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Kết nối tới ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi đã kết nối");
}

// Hàm xử lý khi nhận được tin nhắn MQTT
void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.print("Nhận tin nhắn từ topic: ");
  Serial.println(topic);
  Serial.print("Nội dung: ");
  Serial.println(message);
  if(String(topic) == topicLed){
    int separatorIndex = message.indexOf(";");
    if (separatorIndex != -1) {
      String led = message.substring(0, separatorIndex);
      String state = message.substring(separatorIndex + 1);

      // Chuyển sang chế độ tự động nếu nhận được lệnh "Led1;auto"
      if (led == "Led1" && state == "auto") {
        autoMode = true;
        Serial.println("Chuyển sang chế độ tự động");
      } else if (led == "Led1" && state == "manual") {
        autoMode = false;
        Serial.println("Chuyển sang chế độ thủ công");
        digitalWrite(ledpin1, LOW); 
        light1Status = false;
        client.publish(topicLed, "Led1;OFF");
      }

      if (led == "Led2" && state == "auto") {
        autoMode2 = true;
        Serial.println("Chuyển sang chế độ tự động");
      } else if (led == "Led2" && state == "manual") {
        autoMode2 = false;
        Serial.println("Chuyển sang chế độ thủ công");
        digitalWrite(ledpin2, LOW); 
        light2Status = false;
        client.publish(topicLed, "Led2;OFF");
      }

      // Điều khiển relay 1
      if (led == "Led1" && !autoMode) {
        if (state == "ON") {
          digitalWrite(ledpin1, HIGH);
          light1Status = true;
          Serial.println("Bat den 1");
        } else if (state == "OFF") {
          digitalWrite(ledpin1, LOW);
          light1Status = false;
          Serial.println("Tat den 1");
        }
      }

      // Điều khiển relay 2
      if (led == "Led2" && !autoMode2) {
        if (state == "ON") {
          digitalWrite(ledpin2, HIGH);
          light2Status = true;
          Serial.println("Bat den 2");
        } else if (state == "OFF") {
          digitalWrite(ledpin2, LOW);
          light2Status = false;
          Serial.println("Tat den 2");
        }
      }
    }
  }
  if (String(topic) == mqtt_sub_topic) {
    if (message == "ON") {
      Serial.println("Turning on pump.");
      pump_status = 1;
      // digitalWrite(RELAY_PIN2, LOW);  // Turn on relay
    } 
    else if (message == "OFF") {
      Serial.println("Turning off pump.");
      pump_status = 0;
      digitalWrite(RELAY_PIN2, HIGH); // Turn off relay
    }
    else {
      Serial.println("Invalid operation.");
    }
  }
}

// Hàm kết nối tới MQTT Broker và đăng ký topic
void reconnect() {
  while (!client.connected()) {
    Serial.print("Đang kết nối tới MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Đã kết nối");
      client.subscribe(topicLed);  // Đăng ký topic chính
      client.subscribe(mqtt_sub_topic);
    } else {
      Serial.print("Thất bại, rc=");
      Serial.print(client.state());
      Serial.println(" Thử lại sau 5 giây");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
 
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Cấu hình chân relay là OUTPUT
  pinMode(ledpin1, OUTPUT);
  pinMode(ledpin2, OUTPUT);
  pinMode(lightSensorPin, INPUT);  // Cấu hình chân cảm biến ánh sáng là INPUT
  pinMode(FLAME_SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(RELAY_PIN2, OUTPUT);
  // Mặc định tắt relay
  digitalWrite(ledpin1, LOW);
  digitalWrite(ledpin2, LOW);
  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(RELAY_PIN2, HIGH);
}

void loop() {
  unsigned long current = millis();
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Nếu đang ở chế độ tự động, đọc dữ liệu từ cảm biến ánh sáng
  if (autoMode) {
    int lightValue = digitalRead(lightSensorPin);

    // Kiểm tra giá trị ánh sáng để bật/tắt đèn
    if (lightValue == 1 && !light1Status) {  
      digitalWrite(ledpin1, HIGH);
      light1Status = true;
      client.publish(topicLed, "Led1;ON");  // Gửi trạng thái ON tới MQTT
      Serial.println("Đèn bật do ánh sáng yếu");
    } else if (lightValue == 0 && light1Status) {
      digitalWrite(ledpin1, LOW); 
      light1Status = false;
      client.publish(topicLed, "Led1;OFF"); // Gửi trạng thái OFF của led 1 tới MQTT
      Serial.println("Đèn tắt do ánh sáng đủ");
    }
  }

  if (autoMode2) {
    int lightValue = digitalRead(lightSensorPin);

    // Kiểm tra giá trị ánh sáng để bật/tắt đèn
    if (lightValue == 1 && !light2Status) {  
      digitalWrite(ledpin2, HIGH);
      light2Status = true;
      client.publish(topicLed, "Led2;ON");  
      Serial.println("Đèn bật do ánh sáng yếu");
    } else if (lightValue == 0 && light2Status) {
      digitalWrite(ledpin2, LOW); 
      light2Status = false;
      client.publish(topicLed, "Led2;OFF"); 
      Serial.println("Đèn tắt do ánh sáng đủ");
    }
  }

  int flameDetected = digitalRead(FLAME_SENSOR_PIN);
  if (flameDetected == LOW) {  // Flame detected
    // Serial.println("Flame detected! Blinking light for 5 seconds.");
    if(pump_status == 1) digitalWrite(RELAY_PIN2, LOW);
    else digitalWrite(RELAY_PIN2, HIGH);
    // Publish flame detection message to MQTT
    if(pump_status == 1)client.publish(mqtt_pub_topic, "FireAlarm;YES;ON");
    else client.publish(mqtt_pub_topic, "FireAlarm;YES;OFF");

    // Blink light for 5 seconds
    unsigned long startTime = millis();
    unsigned long previousMillis = 0;
    while (millis() - startTime < 5000) {
      unsigned long currentMillis = millis();

      if (currentMillis - previousMillis >= 500) {
          previousMillis = currentMillis; 

          int relayState = digitalRead(RELAY_PIN); 
          digitalWrite(RELAY_PIN, !relayState);    
      }
    }
  } else {
    // Serial.println("No flame detected. Light is off.");
    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(RELAY_PIN2, HIGH);

    // Publish no flame message to MQTT
    // client.publish(mqtt_pub_topic, "FireAlarm;NO;OFF");
  }

  if(current - previousLog >= delayLog){
    previousLog = current;
    if(light1Status){
      client.publish(topicLed, "Led1;LOGON");
    }
    else {
      client.publish(topicLed, "Led1;LOGOFF");
    }
    if(light2Status){
      client.publish(topicLed, "Led2;LOGON");
    }
    else {
      client.publish(topicLed, "Led2;LOGOFF");
    }
    if(flameDetected == LOW){
      if(pump_status == 1)client.publish(mqtt_pub_topic, "FireAlarm;YES;ON");
      else client.publish(mqtt_pub_topic, "FireAlarm;YES;OFF");
    } else {
      client.publish(mqtt_pub_topic, "FireAlarm;NO;OFF");
    }
  }

}

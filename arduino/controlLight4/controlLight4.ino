#include <WiFi.h>
#include <PubSubClient.h>

// Thông tin kết nối WiFi
const char* ssid = "NTH";
const char* password = "hoanguyen";

// Thông tin MQTT Broker
const char* mqtt_server = "192.168.110.81";

// Chân GPIO điều khiển relay và cảm biến
const int ledpin1 = 19;
const int ledpin2 = 21;
const int lightSensorPin = 32;  // Chân cảm biến ánh sáng

const char* topic = "home/light";  // Topic để nhận lệnh điều khiển

WiFiClient espClient;
PubSubClient client(espClient);

bool light1Status = false;  // Trạng thái đèn hiện tại
bool light2Status = false;
bool lightStatus = false;   // Biến để theo dõi trạng thái ánh sáng
bool autoMode = false;      // Biến để theo dõi chế độ tự động

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
      client.publish(topic, "Led1;OFF");
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
    if (led == "Led2") {
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

// Hàm kết nối tới MQTT Broker và đăng ký topic
void reconnect() {
  while (!client.connected()) {
    Serial.print("Đang kết nối tới MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Đã kết nối");
      client.subscribe(topic);  // Đăng ký topic chính
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
 
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Cấu hình chân relay là OUTPUT
  pinMode(ledpin1, OUTPUT);
  pinMode(ledpin2, OUTPUT);
  pinMode(lightSensorPin, INPUT);  // Cấu hình chân cảm biến ánh sáng là INPUT

  // Mặc định tắt relay
  digitalWrite(ledpin1, LOW);
  digitalWrite(ledpin2, LOW);
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
    Serial.print("Giá trị ánh sáng: ");
    Serial.println(lightValue);


    // Kiểm tra giá trị ánh sáng để bật/tắt đèn
    if (lightValue == 1 && !light1Status) {  
      digitalWrite(ledpin1, HIGH);
      // digitalWrite(ledpin2, HIGH);    // Bật đèn
      light1Status = true;
      // light2Status = true;
      client.publish(topic, "Led1;ON");  // Gửi trạng thái ON tới MQTT
      // client.publish(topic, "Led2;ON");  // Gửi trạng thái ON tới MQTT
      Serial.println("Đèn bật do ánh sáng yếu");
    } else if (lightValue == 0 && light1Status) {
      digitalWrite(ledpin1, LOW); 
      // digitalWrite(ledpin2, LOW);    // Tắt đèn
      light1Status = false;
      // light2Status = false;
      client.publish(topic, "Led1;OFF"); // Gửi trạng thái OFF của led 1 tới MQTT
      // client.publish(topic, "Led2;OFF"); // Gửi trạng thái OFF của led 2 tới MQTT
      Serial.println("Đèn tắt do ánh sáng đủ");
    }
  }

  if(current - previousLog >= delayLog){
    previousLog = current;
    if(light1Status){
      client.publish(topic, "Led1;LOGON");
    }
    else {
      client.publish(topic, "Led1;LOGOFF");
    }
    if(light2Status){
      client.publish(topic, "Led2;LOGON");
    }
    else {
      client.publish(topic, "Led2;LOGOFF");
    }
  }

}

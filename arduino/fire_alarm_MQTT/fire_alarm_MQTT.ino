#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Define pins
#define FLAME_SENSOR_PIN 5  // Pin for flame sensor
#define RELAY_PIN 4         // Pin for relay controlling the light
#define RELAY_PIN2 18       // Additional relay pin

// Wi-Fi credentials
const char* ssid = "NTH";         // Replace with your Wi-Fi SSID
const char* password = "hoanguyen";         // Replace with your Wi-Fi password

// MQTT broker details
const char* mqtt_server = "192.168.110.81";      // Example broker
const int mqtt_port = 1883;
const char* mqtt_pub_topic = "fire_alarm/status"; // Topic for publishing status
const char* mqtt_sub_topic = "fire_alarm/control"; // Topic for subscribing to commands
int pump_status = 0;  // Corrected data type for pump_status

WiFiClient espClient;
PubSubClient client(espClient);

// Callback function for incoming messages on the subscribed topic
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  Serial.println(messageTemp);

  // Act on the message if it matches specific commands
  if (String(topic) == mqtt_sub_topic) {
    if (messageTemp == "ON") {
      Serial.println("Turning on pump.");
      pump_status = 1;
      digitalWrite(RELAY_PIN2, LOW);  // Turn on relay
    } 
    else if (messageTemp == "OFF") {
      Serial.println("Turning off pump.");
      pump_status = 0;
      digitalWrite(RELAY_PIN2, HIGH); // Turn off relay
    }
    else {
      Serial.println("Invalid operation.");
    }
  }
}

void setup() {
  Serial.begin(115200);

  // Initialize pins
  pinMode(FLAME_SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(RELAY_PIN2, OUTPUT);

  // Turn off relay on startup
  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(RELAY_PIN2, HIGH);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");

  // Set up MQTT connection and callback
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  connectToMQTT();
}

void loop() {
  // Reconnect to MQTT if disconnected
  if (!client.connected()) {
    connectToMQTT();
  }
  client.loop();

  int flameDetected = digitalRead(FLAME_SENSOR_PIN);

  if (flameDetected == LOW) {  // Flame detected
    Serial.println("Flame detected! Blinking light for 5 seconds.");
    digitalWrite(RELAY_PIN2, LOW);

    // Publish flame detection message to MQTT
    client.publish(mqtt_pub_topic, "Fire detected!");

    // Blink light for 5 seconds
    unsigned long startTime = millis();
    while (millis() - startTime < 5000) {
      digitalWrite(RELAY_PIN, LOW);
      delay(500);
      digitalWrite(RELAY_PIN, HIGH);
      delay(500);
    }
  } else {
    Serial.println("No flame detected. Light is off.");
    digitalWrite(RELAY_PIN, HIGH);
    digitalWrite(RELAY_PIN2, HIGH);

    // Publish no flame message to MQTT
    client.publish(mqtt_pub_topic, "No fire detected.");
  }

  delay(1000);  // Check again after 1 second
}

// Function to connect to MQTT broker
void connectToMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("ESP32Client")) {  // Set a unique client ID
      Serial.println("connected");

      // Subscribe to the control topic
      client.subscribe(mqtt_sub_topic);
      Serial.print("Subscribed to topic: ");
      Serial.println(mqtt_sub_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(1000);
    }
  }
}

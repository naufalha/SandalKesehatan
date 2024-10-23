#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";
const char* mqtt_server = "your_MQTT_BROKER_IP";

// MQTT client and WiFi settings
WiFiClient espClient;
PubSubClient client(espClient);

// Pin and PWM setup
int motorPin = 15; // Pin connected to the motor
int pwmValue = 0;  // Variable to store the calculated PWM value

// Function to map percentage (0-100) to PWM (0-255)
int percentageToPWM(int percentage) {
  return map(percentage, 0, 100, 0, 255);
}

// MQTT callback function - triggered when a message is received
void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  int percentage = message.toInt();  // Convert the received message to an integer

  // Ensure the percentage is within 0-100 range
  if (percentage >= 0 && percentage <= 100) {
    pwmValue = percentageToPWM(percentage);  // Convert percentage to PWM
    ledcWrite(motorPin, pwmValue);  // Set the PWM output for motor control
  }
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("vibration/strength");  // Subscribe to the MQTT topic for vibration strength
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  // Initialize WiFi and MQTT connection
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Setup PWM for the motor
  ledcAttach(motorPin, 5000, 8);    // New LEDC API: Attach pin with frequency and resolution
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();  // Handle MQTT messages
}

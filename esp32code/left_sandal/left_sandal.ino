#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "your_SSID";  // Replace with your Wi-Fi SSID
const char* password = "your_PASSWORD";  // Replace with your Wi-Fi password
const char* mqtt_server = "your_MQTT_BROKER_IP";  // Replace with your MQTT broker IP

// MQTT client and WiFi settings
WiFiClient espClient;
PubSubClient client(espClient);

const int numVibrators = 8;  // Number of vibration points
int vibrators[numVibrators] = {15, 16, 17, 18, 19, 21, 22, 23};  // GPIO pins for the 8 vibrators
int pwmValue = 0;            // Global PWM value to be set for frequency control
int frequency = 100;         // Default frequency for the vibrators

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

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  // Handle binary data for turning on/off multiple vibrators
  if (String(topic) == "/vibrate/") {
    if (message.length() == numVibrators) {
      for (int i = 0; i < numVibrators; i++) {
        if (message[i] == '1') {
          ledcWrite(i, pwmValue);  // Turn on vibrator
          Serial.print("Vibrator ");
          Serial.print(i);
          Serial.println(" ON");
        } else if (message[i] == '0') {
          ledcWrite(i, 0);  // Turn off vibrator
          Serial.print("Vibrator ");
          Serial.print(i);
          Serial.println(" OFF");
        }
      }
    } else {
      Serial.println("Invalid message length! Must be 8 binary digits.");
    }
  }

  if (String(topic) == "/frequency") {
    // Set the global frequency based on MQTT message
    frequency = message.toInt();
    pwmValue = map(frequency, 1, 1000, 0, 255);  // Map frequency to PWM range (1-1000 Hz)
    Serial.print("Frequency set to ");
    Serial.println(frequency);
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("/vibrate/");   // Subscribe to vibrate control topic
      client.subscribe("/frequency");  // Subscribe to frequency control topic
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
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Initialize the vibrator pins as PWM outputs
  for (int i = 0; i < numVibrators; i++) {
    ledcAttach(vibrators[i], 5000, 8);  // Attach pins with a base frequency of 5 kHz and 8-bit resolution
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();  // Handle MQTT messages

  // No need to modify loop because control happens in the callback
  delay(100);  // Small delay to keep loop stable
}

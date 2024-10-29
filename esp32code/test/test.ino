#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YourNetworkName";  // Replace with your Wi-Fi SSID
const char* password = "YourPassword";  // Replace with your Wi-Fi password
const char* mqtt_server = "192.168.4.1";  // Replace with your MQTT broker IP

// MQTT client and WiFi settings
WiFiClient espClient;
PubSubClient client(espClient);

const int numVibrators = 8;  // Number of vibration points
int vibrators[numVibrators] = {15, 16, 17, 18, 19, 21, 22, 23};  // GPIO pins for the 8 vibrators
int pwmValue = 0;  // Global PWM value for all vibrators (0-255)
bool vibratorState[numVibrators] = {false};  // Stores ON/OFF state for each vibrator

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

  // Handle vibrate control message
  if (String(topic) == "/vibrate/") {
    if (message.length() == numVibrators) {
      for (int i = 0; i < numVibrators; i++) {
        if (message[i] == '1') {
          vibratorState[i] = true;  // Turn vibrator ON
          ledcWrite(vibrators[i], pwmValue);   // Set to current PWM value
          Serial.print("Vibrator ");
          Serial.print(i);
          Serial.println(" ON");
        } else if (message[i] == '0') {
          vibratorState[i] = false;  // Turn vibrator OFF
          ledcWrite(vibrators[i], 0);  // Set PWM to 0
          Serial.print("Vibrator ");
          Serial.print(i);
          Serial.println(" OFF");
        }
      }
    } else {
      Serial.println("Invalid message length! Must be 8 binary digits.");
    }
  }

  // Handle setting PWM value
  if (String(topic) == "/pwm") {
    pwmValue = message.toInt();  // Convert message to integer for PWM
    if (pwmValue < 0) pwmValue = 0;
    if (pwmValue > 255) pwmValue = 255;
    Serial.print("PWM set to ");
    Serial.println(pwmValue);

    // Update all ON vibrators with the new PWM value
    for (int i = 0; i < numVibrators; i++) {
      if (vibratorState[i]) {
        ledcWrite(vibrators[i], pwmValue);  // Apply new PWM to all vibrators that are ON
      }
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("/vibrate/");   // Subscribe to vibrate control topic
      client.subscribe("/pwm");        // Subscribe to PWM control topic
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

  // Initialize PWM for the vibrators
  for (int i = 0; i < numVibrators; i++) {
    ledcAttach(vibrators[i], 5000, 8);  // Attach pin with 5 kHz frequency and 8-bit resolution
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();  // Handle incoming MQTT messages
}

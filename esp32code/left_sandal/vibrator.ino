#include <WiFi.h>
#include <PubSubClient.h>

// Wi-Fi and MQTT server credentials
const char* ssid = "Milos";
const char* password = "11111111";
const char* mqtt_server = "192.168.47.225";

WiFiClient espClient;
PubSubClient client(espClient);

// Define the pins connected to each vibrator
const int vibratorPins[] = {13, 12, 1, 27, 26, 25, 33, 32};
const int numPins = sizeof(vibratorPins) / sizeof(vibratorPins[0]);

// Store the frequency and last toggle time for each vibrator
int frequencies[numPins] = {0};           // Frequency in Hz for each pin
unsigned long lastToggleTimes[numPins] = {0};  // Track the last toggle time
bool vibratorStates[numPins] = {false};    // Current on/off state for each pin

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
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  // Convert the payload to a string
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  // Check if the message is from /sandal/left
  if (String(topic) == "/sandal/left") {
    int colonIndex = message.indexOf(':');
    if (colonIndex != -1) {
      // Extract the pin label and frequency value
      char pinLabel = message.charAt(2);   // Third character for the key (e.g., "a")
      int frequency = message.substring(colonIndex + 1, message.length() - 1).toInt(); // Extract frequency value
      
      int pinIndex = pinLabel - 'a'; // Calculate index from 'a', 'b', etc.
      if (pinIndex >= 0 && pinIndex < numPins) {
        frequencies[pinIndex] = frequency; // Update frequency for the specified vibrator
      }
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("/sandal/left");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  for (int i = 0; i < numPins; i++) {
    pinMode(vibratorPins[i], OUTPUT);
    digitalWrite(vibratorPins[i], LOW);  // Ensure all vibrators are initially off
  }
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long currentMillis = millis();

  // Update each vibrator according to its frequency
  for (int i = 0; i < numPins; i++) {
    if (frequencies[i] > 0) { // Only toggle if frequency is set
      // Calculate the toggle interval for the given frequency
      unsigned long interval = 1000 / (frequencies[i] * 2); // Half-period for on/off

      // Check if it's time to toggle the vibrator state
      if (currentMillis - lastToggleTimes[i] >= interval) {
        vibratorStates[i] = !vibratorStates[i]; // Toggle state
        digitalWrite(vibratorPins[i], vibratorStates[i] ? HIGH : LOW); // Update pin output
        lastToggleTimes[i] = currentMillis; // Reset the last toggle time
      }
    } else {
      // If frequency is 0, ensure the vibrator is off
      digitalWrite(vibratorPins[i], LOW);
      vibratorStates[i] = false;
    }
  }
}

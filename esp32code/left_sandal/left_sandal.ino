#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Milos";
const char* password = "11111111";
const char* mqtt_server = "192.168.47.225";

WiFiClient espClient;
PubSubClient client(espClient);

// Define the pins connected to each vibrator
const int vibratorPins[] = {13, 12, 1, 27, 26, 25, 33, 32};
const int numPins = sizeof(vibratorPins) / sizeof(vibratorPins[0]);

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
    // Parse message in "a:1" format
    char pinLabel = message.charAt(0);    // Pin identifier like 'a', 'b', etc.
    int frequency = message.substring(2).toInt(); // On/off frequency, 1 or 0

    int pinIndex = pinLabel - 'a'; // Calculate index from 'a', 'b', etc.
    if (pinIndex >= 0 && pinIndex < numPins) {
      // Control the corresponding pin based on frequency value
      if (frequency == 1) {
        digitalWrite(vibratorPins[pinIndex], HIGH);  // Turn on vibrator
      } else {
        digitalWrite(vibratorPins[pinIndex], LOW);   // Turn off vibrator
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
}

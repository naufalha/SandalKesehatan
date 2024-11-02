#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Milos";  // Replace with your network SSID
const char* password = "11111111";  // Replace with your network password
const char* mqtt_server = "192.168.132.225";

WiFiClient espClient;
PubSubClient client(espClient);

const int buttonPinRight = 13;
const int buttonPinLeft = 12;
bool lastButtonStateRight = LOW;
bool lastButtonStateLeft = LOW;

void setup() {
  pinMode(buttonPinRight, INPUT_PULLUP);
  pinMode(buttonPinLeft, INPUT_PULLUP);
  
  Serial.begin(115200);
  setupWiFi();
  client.setServer(mqtt_server, 1883);
}

void setupWiFi() {
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
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
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

  bool currentButtonStateRight = !digitalRead(buttonPinRight);
  bool currentButtonStateLeft = !digitalRead(buttonPinLeft);

  if (currentButtonStateRight && currentButtonStateRight != lastButtonStateRight) {
    client.publish("/button/right", "true");
  }
  lastButtonStateRight = currentButtonStateRight;

  if (currentButtonStateLeft && currentButtonStateLeft != lastButtonStateLeft) {
    client.publish("/button/left", "true");
  }
  lastButtonStateLeft = currentButtonStateLeft;
  
  delay(50);  // Debounce delay
}

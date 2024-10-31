#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "YourNetwork";
const char* password = "YourPassword";

// MQTT Broker settings
const char* mqtt_server = "your_mqtt_broker_ip";
const int mqtt_port = 1883;
const char* mqtt_topic = "/sandal/right/button";

// Button pin
const int buttonPin = 15;  // D15

// Variables to handle button state
bool lastButtonState = false;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;  // Adjust this value if needed

// Initialize WiFi and MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  // Initialize button pin
  pinMode(buttonPin, INPUT_PULLUP);
  
  // Connect to WiFi
  setup_wifi();
  
  // Set MQTT broker
  client.setServer(mqtt_server, mqtt_port);
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
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void publishButtonState(bool pressed) {
  String message = pressed ? "{\"pressed\":true}" : "{\"pressed\":false}";
  client.publish(mqtt_topic, message.c_str());
  Serial.print("Published: ");
  Serial.println(message);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Read button state (invert because of pull-up)
  bool currentButtonState = !digitalRead(buttonPin);
  
  // Check if button state has changed
  if (currentButtonState != lastButtonState) {
    // Reset the debouncing timer
    lastDebounceTime = millis();
  }

  // If enough time has passed, check if the state has really changed
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // Only publish if the button state has actually changed
    if (currentButtonState != lastButtonState) {
      publishButtonState(currentButtonState);
      lastButtonState = currentButtonState;
    }
  }

  delay(10);  
} 
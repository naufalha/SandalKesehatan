from machine import Pin
import network
import time
from umqtt.simple import MQTTClient
import json

class RightSandalHandler:
    def __init__(self):
        # WiFi credentials
        self.WIFI_SSID = "YourNetwork"
        self.WIFI_PASSWORD = "YourPassword"
        
        # MQTT settings
        self.MQTT_BROKER = "your_mqtt_broker_ip"
        self.MQTT_PORT = 1883
        self.MQTT_TOPIC = b"/sandal/right/button"
        self.CLIENT_ID = "esp32_right_sandal"
        
        # Button setup (D15 = GPIO15)
        self.button = Pin(15, Pin.IN, Pin.PULL_UP)  # Using pull-up resistor
        self.last_state = None

    def connect_wifi(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
        if not self.wlan.isconnected():
            print(f'Connecting to WiFi network: {self.WIFI_SSID}...')
            self.wlan.connect(self.WIFI_SSID, self.WIFI_PASSWORD)
            
            # Wait for connection with timeout
            max_wait = 10
            while max_wait > 0:
                if self.wlan.isconnected():
                    break
                max_wait -= 1
                print('Waiting for connection...')
                time.sleep(1)
            
            if self.wlan.isconnected():
                print('WiFi connected successfully')
                print('Network config:', self.wlan.ifconfig())
            else:
                print('WiFi connection failed')
                raise Exception('WiFi connection failed')

    def publish_button_state(self):
        current_state = not self.button.value()  # Invert because of pull-up
        
        # Only publish if state has changed
        if current_state != self.last_state:
            self.last_state = current_state
            message = json.dumps({"pressed": current_state})
            print(f"Publishing button state: {message}")
            self.mqtt_client.publish(self.MQTT_TOPIC, message)

    def run(self):
        try:
            # Connect to WiFi
            self.connect_wifi()
            
            # Connect to MQTT broker
            print('Connecting to MQTT broker...')
            self.mqtt_client = MQTTClient(
                self.CLIENT_ID, 
                self.MQTT_BROKER,
                port=self.MQTT_PORT
            )
            self.mqtt_client.connect()
            print('Connected to MQTT broker')
            
            # Main loop
            print('Monitoring button state...')
            while True:
                self.publish_button_state()
                time.sleep(0.1)  # Debounce delay
                
        except Exception as e:
            print('Error:', e)
            
        finally:
            if hasattr(self, 'mqtt_client'):
                self.mqtt_client.disconnect()

from threading import Thread
import time
import json
import paho.mqtt.client as mqtt
import subprocess
from right_sandal.right_sandal_handler import RightSandalHandler

# Global variable to control the start of the vibration detection
start_detection = False

# Callback function for handling MQTT messages
def on_message(client, userdata, message):
    global start_detection
    payload = message.payload.decode()

    if message.topic == "/start" and payload == "detection":
        print("Received 'detection' command on /start. Starting vibration detection...")
        start_detection = True

def mqtt_listener():
    # Initialize MQTT client
    client = mqtt.Client()
    client.on_message = on_message

    # Connect to the local MQTT broker
    client.connect("localhost", 1883)
    client.loop_start()

    # Subscribe to the /start topic
    client.subscribe("/start")
    
    print("Waiting for 'detection' command on /start...")

    # Keep the listener running
    while True:
        time.sleep(1)

def delayed_vibration_detection():
    global start_detection
    # Wait until start_detection is True
    while not start_detection:
        time.sleep(0.1)  # Check every 100ms

    # Start the vibration detection script
    print("Running vibration detection script...")
    subprocess.run(["python3", "detection/vibration_detection.py"])

def main():
    # Initialize the right sandal handler instance
    right_sandal_handler = RightSandalHandler()

    # Create threads for concurrent execution
    handler_thread = Thread(target=right_sandal_handler.run)
    detection_thread = Thread(target=delayed_vibration_detection)
    listener_thread = Thread(target=mqtt_listener)

    # Start threads
    handler_thread.start()
    listener_thread.start()
    detection_thread.start()

    # Wait

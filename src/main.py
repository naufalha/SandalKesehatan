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

    try:
        # Connect to the local MQTT broker
        client.connect("localhost", 1883)
        client.loop_start()
        print("Connected to MQTT broker and waiting for 'detection' command on /start...")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return

    # Subscribe to the /start topic
    client.subscribe("/start")
    
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
    try:
        result = subprocess.run(["python3", "detection/vibration_detection.py"], check=True)
        print("Vibration detection completed:", result)
    except subprocess.CalledProcessError as e:
        print(f"Error running vibration detection script: {e}")

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

    # Wait for all threads to finish
    handler_thread.join()
    listener_thread.join()
    detection_thread.join()

if __name__ == "__main__":
    main()

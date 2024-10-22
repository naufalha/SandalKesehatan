import paho.mqtt.client as mqtt
import time
from datetime import datetime

# MQTT broker information
broker_address = "localhost"  # Change to your broker's IP if remote (e.g., "192.168.x.x")
topic = "time/current"

# Create an MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address)

# Infinite loop to continuously publish time
try:
    while True:
        # Get current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")  # Format: hours:minutes:seconds

        # Publish time to the specified topic
        client.publish(topic, f"Current time: {current_time}")
        print(f"Published: Current time: {current_time}")

        # Wait for 1 second before publishing again
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user.")

# Disconnect from the broker
client.disconnect()

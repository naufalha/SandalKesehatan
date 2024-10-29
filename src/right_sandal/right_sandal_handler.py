import time
import RPi.GPIO as GPIO
from src.utils.mqtt_client import MQTTClient

class RightSandalHandler:
    def __init__(self):
        # Initialize the MQTT client to subscribe to the topic
        self.mqtt_client = MQTTClient("right_sandal_mqtt_node")
        
        # Define GPIO pins for each of the 8 points, e.g., "a" to "h"
        self.vibration_points = {
            "a": 17,
            "b": 18,
            "c": 27,
            "d": 22,
            "e": 23,
            "f": 24,
            "g": 25,
            "h": 5,
        }

        # Initialize GPIO settings
        GPIO.setmode(GPIO.BCM)
        for pin in self.vibration_points.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Start all motors off

    def on_vibration_data(self, data):
        """
        Process each point in the data to control the respective motor.
        Data format: {"a": frequency, "b": frequency, ...}
        """
        for point, frequency in data.items():
            if point in self.vibration_points:
                pin = self.vibration_points[point]
                self.control_vibrator(pin, frequency)

    def control_vibrator(self, pin, frequency):
        """
        Controls a GPIO pin to turn on and off based on the specified frequency.
        """
        if frequency > 0:
            # Turn motor on for a period based on frequency
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1.0 / frequency)  # ON duration based on frequency
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1.0 / frequency)  # OFF duration based on frequency
        else:
            GPIO.output(pin, GPIO.LOW)  # Turn off if frequency is zero

    def start(self):
        """
        Start the MQTT client and listen for data on the /sandal/right topic.
        """
        self.mqtt_client.subscribe("/sandal/right")
        print("Listening for vibration data on /sandal/right...")

        # Continuously check for new data
        while True:
            message = self.mqtt_client.get_data()
            if message:
                try:
                    # Parse message as a dictionary and handle vibration data
                    data = eval(message)  # Evaluate the dictionary message safely
                    self.on_vibration_data(data)
                except Exception as e:
                    print("Error in processing data:", e)
            time.sleep(0.1)  # Polling delay

    def cleanup(self):
        """
        Clean up GPIO resources when done.
        """
        GPIO.cleanup()

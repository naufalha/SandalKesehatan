import time
import RPi.GPIO as GPIO
from src.utils.mqtt_client import MQTTClient

class RightSandalHandler:
    def __init__(self):
        self.mqtt_client = MQTTClient("right_sandal_mqtt_node")
        self.vibration_points = {
            "a": 21,
            "b": 20,
            "c": 16,
            "d": 12,
            "e": 26,
            "f": 13,
            "g": 6,
            "h": 5,
        }
        GPIO.setmode(GPIO.BCM)
        for pin in self.vibration_points.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def control_vibrator(self, pin, frequency):
        if frequency > 0:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1.0 / frequency)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1.0 / frequency)
        else:
            GPIO.output(pin, GPIO.LOW)

    def run(self):
        self.mqtt_client.subscribe("/sandal/right")
        print("Listening for vibration data on /sandal/right...")
        try:
            while True:
                message = self.mqtt_client.get_data()
                if message:
                    try:
                        data = eval(message)
                        for point, frequency in data.items():
                            if point in self.vibration_points:
                                self.control_vibrator(self.vibration_points[point], frequency)
                    except Exception as e:
                        print("Error in processing data:", e)
                time.sleep(0.1)
        finally:
            self.cleanup()

    def cleanup(self):
        GPIO.cleanup()

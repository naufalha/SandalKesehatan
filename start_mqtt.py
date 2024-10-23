import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO_PINS = [17, 18, 27, 22, 23, 24, 25, 4]  # Example GPIO pins, adjust as needed
VIBRATOR_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
pwm_objects = {}

for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm_objects[pin] = GPIO.PWM(pin, 100)  # Create PWM object for each pin
    pwm_objects[pin].start(0)  # Start PWM with 0% duty cycle

# MQTT settings
MQTT_BROKER = "localhost"  # Change this if your broker is on a different machine
MQTT_PORT = 1883
MQTT_TOPIC_ONOFF = "raspi/vibrator/onoff"
MQTT_TOPIC_STRENGTH = "raspi/vibrator/strength"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC_ONOFF)
    client.subscribe(MQTT_TOPIC_STRENGTH)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")
    
    if msg.topic == MQTT_TOPIC_ONOFF:
        handle_onoff_message(payload)
    elif msg.topic == MQTT_TOPIC_STRENGTH:
        handle_strength_message(payload)

def handle_onoff_message(payload):
    try:
        states = [bool(int(state)) for state in payload.split(',')]
        if len(states) != 8:
            raise ValueError("Expected 8 boolean values")
        
        for pin, state, label in zip(GPIO_PINS, states, VIBRATOR_LABELS):
            if state:
                pwm_objects[pin].ChangeDutyCycle(100)  # Turn on at full strength
                print(f"Vibrator {label} (GPIO {pin}) is ON at 100% strength")
            else:
                pwm_objects[pin].ChangeDutyCycle(0)  # Turn off
                print(f"Vibrator {label} (GPIO {pin}) is OFF")
    except ValueError as e:
        print(f"Invalid message format for on/off: {e}")
        print("Use 8 comma-separated boolean values (e.g., '1,0,1,0,1,0,1,0')")

def handle_strength_message(payload):
    try:
        pin_number, strength = map(int, payload.split(','))
        if 0 <= pin_number < len(GPIO_PINS) and 0 <= strength <= 100:
            pin = GPIO_PINS[pin_number]
            label = VIBRATOR_LABELS[pin_number]
            pwm_objects[pin].ChangeDutyCycle(strength)
            print(f"Vibrator {label} (GPIO {pin}) strength set to {strength}%")
        else:
            print(f"Invalid pin number or strength value: {payload}")
    except ValueError:
        print("Invalid message format for strength. Use 'pin_number,strength' (e.g., '0,50')")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    for pwm in pwm_objects.values():
        pwm.stop()
    GPIO.cleanup()
    client.disconnect()

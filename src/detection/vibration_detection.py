import time
import json
import paho.mqtt.client as mqtt

# Global variables for button press detection
left_button_pressed = False
right_button_pressed = False

# Callback functions to handle button press events from MQTT
def on_message(client, userdata, message):
    global left_button_pressed, right_button_pressed
    topic = message.topic
    payload = json.loads(message.payload.decode())
    
    if topic == "/button/left" and payload:
        left_button_pressed = True
    elif topic == "/button/right" and payload:
        right_button_pressed = True

# Detection function for neuropathy test
def perform_vibration_test(client):
    global left_button_pressed, right_button_pressed
    
    # Define vibration points for each sandal
    left_points = ["a", "b", "c", "d", "e", "f", "g", "h"]
    right_points = ["a", "b", "c", "d", "e", "f", "g", "h"]
    
    # Starting frequency, increment step, max frequency, and step duration
    start_freq = 5      # Hz
    freq_step = 5       # Hz
    max_freq = 65       # Hz
    neuropathy_threshold = 25  # Hz threshold for neuropathy
    step_duration = 2    # seconds

    # Initialize results dictionary to track neuropathy status for each point
    results = {
        "kanan": {point: 0 for point in right_points},
        "kiri": {point: 0 for point in left_points}
    }

    # Iterate over right and left sandal points
    for point in right_points:
        freq = start_freq
        right_button_pressed = False
        print(f"Testing right point {point}...")

        # Test frequencies until button press or max frequency reached
        while not right_button_pressed and freq <= max_freq:
            client.publish("/sandal/right", json.dumps({point: freq}))
            print(f"Right {point}: {freq} Hz")
            time.sleep(step_duration)

            # Increase frequency for next cycle
            freq += freq_step

        # Turn off the vibrator after finishing the test for this point
        client.publish("/sandal/right", json.dumps({point: 0}))
        time.sleep(0.5)  # Small delay to ensure message is sent

        # Check if patient felt the vibration above the neuropathy threshold
        felt_vibration = right_button_pressed and (freq - freq_step) > neuropathy_threshold
        results["kanan"][point] = int(felt_vibration)  # 1 for positive, 0 for negative neuropathy

    for point in left_points:
        freq = start_freq
        left_button_pressed = False
        print(f"Testing left point {point}...")

        # Test frequencies until button press or max frequency reached
        while not left_button_pressed and freq <= max_freq:
            client.publish("/sandal/left", json.dumps({point: freq}))
            print(f"Left {point}: {freq} Hz")
            time.sleep(step_duration)

            # Increase frequency for next cycle
            freq += freq_step

        # Turn off the vibrator after finishing the test for this point
        client.publish("/sandal/left", json.dumps({point: 0}))
        time.sleep(0.5)  # Small delay to ensure message is sent

        # Check if patient felt the vibration above the neuropathy threshold
        felt_vibration = left_button_pressed and (freq - freq_step) > neuropathy_threshold
        results["kiri"][point] = int(felt_vibration)  # 1 for positive, 0 for negative neuropathy

    # Publish the results to the /nerve topic
    client.publish("/nerve", json.dumps(results))
    print(f"Published neuropathy test results to /nerve: {json.dumps(results)}")

def main():
    # Initialize MQTT client
    client = mqtt.Client()
    client.on_message = on_message
    
    # Connect to local MQTT broker
    client.connect("localhost", 1883)
    client.loop_start()
    
    # Subscribe to button press topics
    client.subscribe("/button/left")
    client.subscribe("/button/right")
    
    # Perform the neuropathy test
    perform_vibration_test(client)

    # Stop MQTT loop after the test is complete
    client.loop_stop()

if __name__ == "__main__":
    main()

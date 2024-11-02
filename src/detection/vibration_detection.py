import time
import json

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

    # Track results to calculate diagnosis percentage
    total_points = len(left_points) + len(right_points)
    positive_results = 0

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

        # Determine if the patient felt it above the threshold
        felt_vibration = right_button_pressed and (freq - freq_step) > neuropathy_threshold
        client.publish("/nerve/right", json.dumps({point: felt_vibration}))
        print(f"Published to /nerve: {point} felt {felt_vibration}")

        # Count positive result if neuropathy detected
        if felt_vibration:
            positive_results += 1

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

        # Determine if the patient felt it above the threshold
        felt_vibration = left_button_pressed and (freq - freq_step) > neuropathy_threshold
        client.publish("/nerve/left", json.dumps({point: felt_vibration}))
        print(f"Published to /nerve: {point} felt {felt_vibration}")

        # Count positive result if neuropathy detected
        if felt_vibration:
            positive_results += 1

    # Calculate and publish diagnosis percentage
    diagnosis_percentage = (positive_results / total_points) * 100
    client.publish("/diagnose", json.dumps({"diagnosis_percentage": diagnosis_percentage}))
    print(f"Diagnosis completed. Published to /diagnose: {diagnosis_percentage}% neuropathy detected.")

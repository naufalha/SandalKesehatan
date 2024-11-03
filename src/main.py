from threading import Thread
import time
from right_sandal.right_sandal_handler import RightSandalHandler
from detection.vibration_detection import VibrationDetection

def delayed_vibration_detection(vibration_detection):
    # Wait for 10 seconds before starting the vibration detection
    time.sleep(10)
    vibration_detection.run()

def main():
    # Initialize instances
    right_sandal_handler = RightSandalHandler()
    vibration_detection = VibrationDetection()

    # Create threads for concurrent execution
    handler_thread = Thread(target=right_sandal_handler.run)
    detection_thread = Thread(target=delayed_vibration_detection, args=(vibration_detection,))

    # Start threads
    handler_thread.start()
    detection_thread.start()

    # Wait for both threads to finish
    handler_thread.join()
    detection_thread.join()

if __name__ == "__main__":
    main()

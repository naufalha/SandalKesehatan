from right_sandal.right_sandal_handler import RightSandalHandler
from detection.vibration_detection import perform_vibration_test

def main():
    right_sandal_handler = RightSandalHandler()
    right_sandal_handler.run()
    vibration_detection = VibrationDetection()
    vibration_detection.run()
    
if __name__ == "__main__":
    main()

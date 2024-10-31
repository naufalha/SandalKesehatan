import RPi.GPIO as GPIO
import time

class GPIOTester:
    def __init__(self):
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        self.valid_pins = [21, 20, 16, 12, 26, 19, 13, 6, 5]
        
        # Initialize all pins as output
        for pin in self.valid_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        print("\nGPIO Test initialized")
        print("Valid GPIO pins:", self.valid_pins)
        self.print_pin_status()

    def print_pin_status(self):
        print("\nCurrent GPIO Status:")
        for pin in self.valid_pins:
            state = GPIO.input(pin)
            print(f"GPIO {pin}: {'ON' if state else 'OFF'}")

    def toggle_pin(self, pin_number):
        if pin_number in self.valid_pins:
            current_state = GPIO.input(pin_number)
            GPIO.output(pin_number, not current_state)
            print(f"\nToggled GPIO {pin_number} {'OFF' if current_state else 'ON'}")
            self.print_pin_status()
        else:
            print(f"\nInvalid GPIO pin. Valid pins are: {self.valid_pins}")

    def cleanup(self):
        print("\nCleaning up GPIO...")
        GPIO.cleanup()

def main():
    tester = GPIOTester()
    
    try:
        while True:
            print("\nCommands:")
            print("- Enter GPIO number to toggle (e.g., '21')")
            print("- Enter 'status' to see current status")
            print("- Enter 'q' to quit")
            
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'q':
                break
            elif command == 'status':
                tester.print_pin_status()
            else:
                try:
                    pin_number = int(command)
                    tester.toggle_pin(pin_number)
                except ValueError:
                    print("\nInvalid command. Please enter a valid GPIO number or command.")
    
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        tester.cleanup()
        print("Program ended")

if __name__ == "__main__":
    main()
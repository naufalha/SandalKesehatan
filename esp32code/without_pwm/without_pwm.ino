const int motorPin = 15;  // Define GPIO pin 15 for the motor
float freq;               // Variable to store frequency
unsigned long delayTime;  // Delay in microseconds
bool motorState = false;  // Motor state to toggle on/off

void setup() {
  Serial.begin(115200);         // Initialize serial communication
  pinMode(motorPin, OUTPUT);     // Set motorPin as output
  digitalWrite(motorPin, LOW);   // Initialize the motor as off
  Serial.println("Enter frequency in Hz (1-60) or type '0' to stop:");
}

void loop() {
  if (Serial.available()) {
    freq = Serial.parseFloat();  // Read the input frequency
    if (freq == 0) {
      digitalWrite(motorPin, LOW); // Turn off the motor
      Serial.println("Motor stopped.");
      return;
    }
    if (freq < 1 || freq > 65) {
      Serial.println("Please enter a frequency between 1 and 60 Hz.");
      return;
    }

    delayTime = (1000000 / (2 * freq));  // Calculate delay in microseconds for half-period
    Serial.print("Running motor at ");
    Serial.print(freq);
    Serial.println(" Hz.");
  }

  // Toggle motor state at the calculated frequency
  motorState = !motorState;              // Change motor state
  digitalWrite(motorPin, motorState);    // Set motor state
  delayMicroseconds(delayTime);          // Delay based on frequency
}

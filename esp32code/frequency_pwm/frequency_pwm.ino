const int motorPin = 15;       // Pin connected to the motor
const int resolution = 8;      // 8-bit resolution (0-255)
int frequency = 100;           // Default frequency (can be changed via Serial input)
int onTime, offTime;

void setup() {
  Serial.begin(115200);
  
  // Attach PWM for the motor pin with an initial frequency
  ledcAttach(motorPin, 5000, resolution); // Setup PWM
  Serial.println("Enter a frequency (in Hz) via the Serial Monitor to change the motor speed:");
}

void loop() {
  // Check if user input is available
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read the input until newline
    frequency = input.toInt();  // Convert input to integer

    // Ensure the input frequency is valid
    if (frequency >= 1 && frequency <= 1000) {
      Serial.print("Vibrating at ");
      Serial.print(frequency);
      Serial.println(" Hz");
    } else {
      Serial.println("Please enter a valid frequency between 1 Hz and 1000 Hz.");
      return; // Exit if the frequency is invalid
    }
  }

  // Calculate on and off times based on the input frequency
  onTime = 1000 / (2 * frequency);  // Calculate on time for a 50% duty cycle
  offTime = onTime;                 // Off time is the same as on time for 50% duty cycle

  // Vibrate indefinitely at the set frequency
  ledcWrite(motorPin, 255);  // Turn motor on
  delay(onTime);             // Wait for onTime duration
  ledcWrite(motorPin, 0);    // Turn motor off
  delay(offTime);            // Wait for offTime duration
}

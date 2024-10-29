const int motorPin = 15;       // Pin connected to the motor
const int resolution = 8;      // 8-bit resolution (0-255)
int pwmValue = 0;              // Variable to hold the PWM value

void setup() {
  Serial.begin(115200);
  
  // Attach PWM for the motor pin with an initial frequency
  ledcAttach(motorPin, 5000, resolution); // Setup PWM with 5 kHz frequency
  Serial.println("Enter a PWM value (0-255) via the Serial Monitor to change the motor speed:");
}

void loop() {
  // Check if user input is available
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Read the input until newline
    pwmValue = input.toInt();  // Convert input to integer

    // Ensure the input PWM value is valid
    if (pwmValue >= 0 && pwmValue <= 255) {
      ledcWrite(motorPin, pwmValue); // Set the PWM value
      Serial.print("Vibrating at PWM: ");
      Serial.println(pwmValue);
    } else {
      Serial.println("Please enter a valid PWM value between 0 and 255.");
    }
  }

  // You can add any additional logic here if needed
}

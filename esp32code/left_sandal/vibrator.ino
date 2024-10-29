#include <Arduino.h>

const int motorPin = 15; // Your motor pin
const int pwmChannel = 0;
const int pwmFrequency = 5000; // Frequency in Hz, adjust as necessary
const int pwmResolution = 8; // 8-bit resolution, so duty cycle goes from 0 to 255

void setup() {
  ledcSetup(pwmChannel, pwmFrequency, pwmResolution); // Configure PWM channel
  ledcAttachPin(motorPin, pwmChannel); // Attach the motor pin to the PWM channel
}

void loop() {
  for (int dutyCycle = 160; dutyCycle <= 255; dutyCycle += 5) {
    ledcWrite(pwmChannel, dutyCycle); // Set PWM duty cycle
    delay(1000); // Wait for 1 second
  }
  ledcWrite(pwmChannel, 0); // Turn off motor
  delay(5000); // Wait 5 seconds before repeating the test
}

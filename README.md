# SandalKesehatan
sandal kesehatan
# Raspberry Pi Vibration Control System

This project implements a vibration control system using a Raspberry Pi, MQTT, and PWM-controlled vibration motors. It allows for remote control of 8 vibration points, including on/off functionality and adjustable vibration strength.

## Features

- Control 8 individual vibration points
- Toggle vibration points on/off
- Adjust vibration strength (0-100%)
- MQTT communication for remote control

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- 8 vibration motors
- Appropriate power supply for the motors
- MQTT broker (e.g., Mosquitto)

## Software Requirements

- Python 3
- RPi.GPIO library
- paho-mqtt library

## Installation

1. Clone this repository to your Raspberry Pi.
2. Install the required Python libraries:
   ```
   pip install RPi.GPIO paho-mqtt
   ```
3. Ensure an MQTT broker is running (either on the Raspberry Pi or another accessible machine).

## Configuration

1. Edit the `GPIO_PINS` list in `start_mqtt.py` to match your GPIO pin configuration.
2. If necessary, update the `MQTT_BROKER` and `MQTT_PORT` variables to point to your MQTT broker.

## Usage

Run the script:

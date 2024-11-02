Creating a structured documentation for your project will help clarify the purpose, setup, usage, and structure of the code. Here’s a draft for the documentation, including sections for an overview, installation, directory structure, and usage.

---

# Sandal Kesehatan Project

## Overview

The **Sandal Kesehatan Project** is designed to test neuropathy in patients by using a pair of sandals equipped with vibration motors. Each point on the sandal vibrates at increasing frequencies to determine the patient’s sensitivity. The patient can indicate if they feel the vibration by pressing a button. This response data is used to calculate a diagnosis, which indicates the percentage of points where neuropathy is detected.

The project uses an ESP32 microcontroller for the left sandal and a Raspberry Pi for the right sandal. Communication is handled via MQTT, with topics for vibration control and button responses.

## Project Components

- **ESP32 (Left Sandal):** Controls vibration points and sends data over MQTT for the left sandal.
- **Raspberry Pi (Right Sandal):** Manages the right sandal’s vibration points and processes button responses.
- **MQTT Broker:** Facilitates communication between devices, publishing vibration frequencies and receiving button response data.

## Installation

### Prerequisites

1. **Hardware**: ESP32, Raspberry Pi (Zero or other models), small 5V vibration motors, and necessary wiring.
2. **Software**:
   - Install `mosquitto` or another MQTT broker on the Raspberry Pi.
   - Install Python 3 on the Raspberry Pi.
   - Install the necessary Python libraries.

### Setting Up

1. Clone the repository on your Raspberry Pi:
   ```bash
   git clone https://github.com/naufalha/SandalKesehatan.git
   cd SandalKesehatan
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MQTT broker (e.g., Mosquitto) on the Raspberry Pi, or ensure the MQTT server is accessible by all devices.

### Configuration

Configure the following MQTT settings in your code files as needed:

- **MQTT Server IP**: `192.168.47.225`
- **Topics**:
  - `/sandal/left` and `/sandal/right`: For sending vibration frequencies.
  - `/button/left` and `/button/right`: For receiving button responses.
  - `/nerve`: For publishing detection results after each point.
  - `/diagnose`: For publishing the final neuropathy diagnosis percentage.

## Directory Structure

```plaintext
src
├── detection            # Contains functions for neuropathy detection.
├── right_sandal         # Code for handling the right sandal's vibration control.
│   └── utils            # Utility files specific to the right sandal.
├── terapi               # Therapy-related functions and logic.
└── utils                # Shared utilities across the project.
main.py                  # Entry point to run the neuropathy test.
```

## Usage

### Running the Project

1. Start the MQTT broker if not already running.
2. Run `main.py` on the Raspberry Pi:
   ```bash
   python3 main.py
   ```

   This script initializes the `RightSandalHandler` class, which manages vibration point testing, listens for button responses, and publishes diagnostic results.

### Vibration Testing Process

1. **Vibration Steps**: Each vibration point begins vibrating at 5 Hz, increasing by 5 Hz every 2 seconds, up to a maximum of 65 Hz.
2. **Button Press Detection**: If the patient feels the vibration, they press a button, which publishes `true` to `/button/left` or `/button/right`.
3. **Diagnosis**: After testing all points, the system calculates the percentage of points where neuropathy is detected (button press above 25 Hz) and publishes this percentage to `/diagnose`.

### Example Workflow

1. **Patient Test**: Patient wears the sandals, and the vibration test starts from point "a" and proceeds through each point.
2. **Patient Feedback**: If the patient feels a vibration, they press the button, and this is logged.
3. **Results Calculation**: The system evaluates the patient’s responses and diagnoses neuropathy based on a threshold frequency (25 Hz).
4. **Final Diagnosis**: The percentage of detected neuropathy points is published to the `/diagnose` topic.

## Future Improvements

- **Adjustable Frequency Parameters**: Allow configuration of starting frequency, step size, and max frequency.
- **Data Logging**: Store results in a database for longitudinal studies.
- **Mobile App Integration**: Visualize results and monitor progress via a mobile app.

## License

[Specify License Here]

---

This documentation covers the main aspects of your project and should be updated as new features or changes are added to the project. Let me know if you'd like further details on specific sections!
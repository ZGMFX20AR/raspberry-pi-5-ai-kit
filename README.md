# Human Notification System Using Raspberry Pi AI Kit and Cytron Maker Pi Pico

This project demonstrates a Human Notification System using the newly launched Raspberry Pi AI Kit and the Cytron Maker Pi Pico. The system detects the presence of a person and provides visual and audio notifications in real-time.

## Overview

In this project, we utilize the high-performance Hailo-8L AI accelerator module from the Raspberry Pi AI Kit for efficient object detection and the Cytron Maker Pi Pico for handling audio and RGB LED notifications. The project is divided into three main components:

1. **Client Code (CircuitPython)**: Connects to a Wi-Fi network, receives data from the server, and controls the RGB LED and audio notifications.
2. **Server Code (Python)**: Sends data to the client based on object detection results.
3. **Background Processing Script (Bash)**: Monitors object detection results and updates the server with relevant data.

## Component List

- **Raspberry Pi 5**: Runs the server code and the Raspberry Pi AI Kit.
- **Raspberry Pi AI Kit**: Runs the YOLO object detection model efficiently.
- **Raspberry Pi Camera Module 3 with Cable**: Captures the video feed for object detection.
- **Maker Pi Pico Base with Raspberry Pi Pico W**: Manages the audio storage, speaker interfacing, and RGB LED.
- **Speaker**: Provides audio notifications.
- **SD Card**: Stores audio files.
- **NVMe SSD (Optional)**: For faster boot and operation. Requires an M.2 to USB adapter for USB boot.
- **Additional Tools and Accessories**: 27-Watt PD power supply for Raspberry Pi 5, internet connection, heatsinks or cooling fan, and a case for the Raspberry Pi.


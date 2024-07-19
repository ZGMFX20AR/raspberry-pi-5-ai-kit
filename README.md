Human Notification System Using Raspberry Pi AI Kit and Cytron Maker Pi Pico
This project demonstrates a Human Notification System using the newly launched Raspberry Pi AI Kit and the Cytron Maker Pi Pico. The system detects the presence of a person and provides visual and audio notifications in real-time.

Overview
In this project, we utilize the high-performance Hailo-8L AI accelerator module from the Raspberry Pi AI Kit for efficient object detection and the Cytron Maker Pi Pico for handling audio and RGB LED notifications. The project is divided into three main components:

Client Code (CircuitPython): Connects to a Wi-Fi network, receives data from the server, and controls the RGB LED and audio notifications.
Server Code (Python): Sends data to the client based on object detection results.
Background Processing Script (Bash): Monitors object detection results and updates the server with relevant data.
Component List
Raspberry Pi 5: Runs the server code and the Raspberry Pi AI Kit.
Raspberry Pi AI Kit: Runs the YOLO object detection model efficiently.
Raspberry Pi Camera Module 3 with Cable: Captures the video feed for object detection.
Maker Pi Pico Base with Raspberry Pi Pico W: Manages the audio storage, speaker interfacing, and RGB LED.
Speaker: Provides audio notifications.
SD Card: Stores audio files.
NVMe SSD (Optional): For faster boot and operation. Requires an M.2 to USB adapter for USB boot.
Additional Tools and Accessories: 27-Watt PD power supply for Raspberry Pi 5, internet connection, heatsinks or cooling fan, and a case for the Raspberry Pi.
Clone Repository
To get started, clone the repository using the following command:

bash
Copy code
git clone https://github.com/ZGMFX20AR/raspberry-pi-5-ai-kit.git
Setting Up the Client Side
Note: This section requires the CircuitPython library which can be downloaded here.

Insert an SD card containing the audio file (to create the audio file, you may follow this tutorial).
Connect your Raspberry Pi Pico W to your Raspberry Pi 5.
Navigate to the cloned folder:
bash
Copy code
cd raspberry-pi-5-ai-kit/PersonDetection/code.py
Copy code.py to the Raspberry Pi Pico W.
Open code.py using Thonny IDE, replace the ssid, password, and server_ip, then save.
Setting Up the Server Side
Note: This section requires a pre-installed Raspberry Pi AI Kit hardware and software components which can be found here.

Open terminal and navigate to the directory:
bash
Copy code
cd raspberry-pi-5-ai-kit/PersonDetection
Make the script executable:
bash
Copy code
chmod +x camera_monitor.sh
Run the server code:
bash
Copy code
python3 server.py
Running All Components
With the server running, open another terminal and run:
bash
Copy code
./camera_monitor.sh
Note: If the camera view window does not appear, ensure the directory of the .json file matches your file directory. You may need to edit the camera_monitor.sh script.

Open Thonny with the Raspberry Pi Pico W and run code.py.
Explanation of the Code
Bash Script: camera_monitor.sh
Monitors the object detection results from the camera feed.
Updates the server with relevant data in real-time.
Server Code: server.py
Listens for connections from the client.
Sends data to the client when a person is detected in the camera feed.
Client Code: code.py
Connects to a Wi-Fi network and communicates with the server.
Controls the RGB LED and audio notifications based on the data received from the server.
Conclusion
By following this tutorial and assembling the specified components, you will create an effective Human Notification System using computer vision and AI capabilities. This project provides a hands-on introduction to integrating AI for real-time object detection and controlling physical hardware like RGB LEDs and speakers.

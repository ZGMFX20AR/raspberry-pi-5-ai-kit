import board
import neopixel
import wifi
import socketpool
import time
import busio
import sdcardio
import storage
import audiocore
import audiopwmio

# SD Card Configuration
DAC = audiopwmio.PWMAudioOut(left_channel=board.GP18, right_channel=board.GP19)
SPI = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
CS = board.GP15
SD = sdcardio.SDCard(SPI, CS)
VFS = storage.VfsFat(SD)
storage.mount(VFS, '/sd')

# Audio Configuration
AUDIO_1 = open("/sd/Attention.wav", "rb")
Alarm = audiocore.WaveFile(AUDIO_1)     

# Wi-Fi credentials
ssid = ""        # Replace with your Wi-Fi SSID
password = ""  # Replace with your Wi-Fi password

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
wifi.radio.connect(ssid, password)
print("Connected to Wi-Fi")

# NeoPixel setup
pixel_pin = board.GP28
num_pixels = 1  # Number of NeoPixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)

# Server information
server_ip = ""  # Replace with the server's IP address
server_port = 6789

def connect_to_server(ip, port):
    pool = socketpool.SocketPool(wifi.radio)
    sock = pool.socket()
    addr = pool.getaddrinfo(ip, port)[0][-1]
    sock.connect(addr)
    return sock

def light_up_pixels(color):
    for i in range(num_pixels):
        pixels[i] = color
    pixels.show()

def main():
    buffer = bytearray(1024)  # Pre-allocate a buffer for incoming data
    last_received_time = time.monotonic()  # Track the last received data time
    last_played_time = 0  # Track the last time the alarm was played
    cooldown = 5  # Cooldown period in seconds
    timeout = 5  # 5 seconds timeout for no data received

    while True:
        sock = None
        try:
            sock = connect_to_server(server_ip, server_port)
            print("Connected to server")
            sock.setblocking(False)  # Set the socket to non-blocking mode
            while True:
                try:
                    bytes_received = sock.recv_into(buffer, 1024)
                    if bytes_received > 0:
                        data = buffer[:bytes_received].decode('utf-8')
                        print(f"Received: {data}")
                        # Send confirmation string to client
                        sock.sendall(b"Received data successfully")
                        current_time = time.monotonic()
                        if "person" in data:
                            light_up_pixels((255, 0, 0))  # Red for "person"
                            last_received_time = current_time  # Update the last received time
                            if current_time - last_played_time >= cooldown:  # Check cooldown
                                if not DAC.playing:  # Play alarm sound if not already playing
                                    DAC.play(Alarm)
                                    last_played_time = current_time  # Update last played time
                        else:
                            last_received_time = current_time  # Update the last received time
                    else:
                        current_time = time.monotonic()
                        if current_time - last_received_time > timeout:
                            light_up_pixels((0, 255, 0))  # Green when no "person" message within timeout
                            if DAC.playing:
                                DAC.stop()  # Stop the alarm if no "person" message within timeout
                        time.sleep(0.1)  # Short sleep to avoid busy-waiting
                except OSError as e:
                    if e.errno == 11:  # Resource temporarily unavailable (EAGAIN)
                        current_time = time.monotonic()
                        if current_time - last_received_time > timeout:
                            light_up_pixels((0, 255, 0))  # Green when no "person" message within timeout
                            if DAC.playing:
                                DAC.stop()  # Stop the alarm if no "person" message within timeout
                        time.sleep(0.1)  # Short sleep to avoid busy-waiting
                    else:
                        print(f"Socket error while receiving data: {e}")
                        break
                
                time.sleep(0.1)  # Short sleep to avoid busy-waiting
                
        except OSError as e:
            print(f"Socket error: {e}")
        finally:
            if sock is not None:
                sock.close()
                print("Disconnected from server")
            light_up_pixels((0, 0, 255))  # Blue when no connection to the server
            if DAC.playing:
                DAC.stop()  # Turn off alarm
            time.sleep(2)  # Wait before attempting to reconnect

if __name__ == "__main__":
    main()

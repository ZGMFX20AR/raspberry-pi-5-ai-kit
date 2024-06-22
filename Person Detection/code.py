import board
import neopixel
import wifi
import socketpool
import time

# Wi-Fi credentials
ssid = "Fsociety"        # Replace with your Wi-Fi SSID
password = "f5f4f3f2f1"  # Replace with your Wi-Fi password

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
wifi.radio.connect(ssid, password)
print("Connected to Wi-Fi")

# NeoPixel setup
pixel_pin = board.GP0
num_pixels = 8  # Number of NeoPixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)

# Server information
server_ip = "192.168.87.37"  # Replace with the server's IP address
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
    timeout = 5  # 5 seconds timeout for no data received

    while True:
        sock = None
        try:
            sock = connect_to_server(server_ip, server_port)
            print("Connected to server")
            while True:
                try:
                    sock.settimeout(timeout)  # Set a timeout for receiving data
                    bytes_received = sock.recv_into(buffer, 1024)
                    if bytes_received == 0:
                        break
                    data = buffer[:bytes_received].decode('utf-8')
                    print(f"Received: {data}")
                    # Send confirmation string to client
                    sock.sendall(b"Received data successfully")
                    if "person" in data:
                        light_up_pixels((255, 0, 0))  # Red for "person"
                        last_received_time = time.monotonic()  # Update the last received time
                    time.sleep(0.2)  # Match the server's sending frequency
                except OSError as e:
                    # Check if the error is a timeout
                    if e.errno == 116:  # 116 is the error number for timeout
                        current_time = time.monotonic()
                        if current_time - last_received_time > timeout:
                            light_up_pixels((0, 0, 255))  # Blue when no signal received
                    else:
                        print(f"Socket error while receiving data: {e}")
                        break
        except OSError as e:
            print(f"Socket error: {e}")
        finally:
            if sock is not None:
                sock.close()
                print("Disconnected from server")
            light_up_pixels((0, 0, 255))  # Blue when no connection to the server
            time.sleep(2)  # Wait before attempting to reconnect

if __name__ == "__main__":
    main()

import socket
import time
import re

# Function to send signals if 'person' is detected in the file
def send_signals(client_socket):
    while True:
        try:
            with open('objects.txt', 'r') as f:
                output = f.read()
            if re.search('person', output):
                client_socket.send(output.encode('utf-8'))
                print("Signal sent")
            time.sleep(0.2)  # Send signal every .2 seconds
        except OSError:
            print("Connection closed while sending signals")
            break

# Main function to handle connections
def main():
    # Setup the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 6789))
    server_socket.listen(1)
    print("Server is listening on port 6789")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")
            send_signals(client_socket)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            print("Connection closed")

if __name__ == "__main__":
    main()


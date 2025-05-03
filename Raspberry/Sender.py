import os
import socket
import time
import subprocess
laptop_ip = "Change-to-your-Laptor's-IP"
laptop_port = 5000
while True:
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"frame_{timestamp}.jpg"
        filepath = f"/home/karthick/Downloads/{filename}"
        os.system(f"fswebcam -q -r 640x480 --no-banner {filepath}")
        print(f"Captured frame: {filename}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((laptop_ip, laptop_port))
            client_socket.sendall(filename.encode())
            print(f"Sent filename to laptop: {filename}")
            response = client_socket.recv(1024).decode()
            print(f"Received response from laptop: {response}")
        if response != "Null":
                os.system(f"espeak '{response}' &")
        time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")
        break

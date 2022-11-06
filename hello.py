print("hello world")

import socket

HOST = "31.204.152.209"  # The server's hostname or IP address
PORT = 6667  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"CAP LS")
    data = s.recv(1024)

print(f"Received {data!r}")


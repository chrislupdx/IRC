
def main():
    print("hello world")

import socket

class baseCall():
    def __init__(self):
        self.HOST = "31.204.152.209"  # The server's hostname or IP address
        self.PORT = 6667  # The port used by the server

    def callsocket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b"CAP LS\r\n")
            data = s.recv(1024)
        print(f"Received {data!r}")


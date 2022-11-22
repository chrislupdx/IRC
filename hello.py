print("hello world")

import socket
from time import sleep

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

"""
Frame 165: 120 bytes on wire (960 bits), 120 bytes captured (960 bits) on interface en0, id 0
Ethernet II, Src: Apple_2c:44:f1 (8c:85:90:2c:44:f1), Dst: ZyxelCom_81:99:0a (54:83:3a:81:99:0a)
Internet Protocol Version 4, Src: 192.168.0.4, Dst: 31.204.152.209
Transmission Control Protocol, Src Port: 54958, Dst Port: 6667, Seq: 9, Ack: 111, Len: 54
Internet Relay Chat
    Request: NICK fiend
        Command: NICK
        Command parameters
            Parameter: fiend
    Request: USER fiend fiend irc.rizon.net :realname
        Command: USER
        Command parameters
            Parameter: fiend
            Parameter: fiend
            Parameter: irc.rizon.net
        Trailer: realname
"""
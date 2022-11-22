import socket
from time import sleep
import selectors
import sys
from threading import Thread

HOST, PORT = sys.argv[1], int(sys.argv[2])

G_quit = False
QUITMSG = "quit"

def readInput(s):
    global G_quit
    global QUITMSG
    while not G_quit:
        usrMsg = input()
        if usrMsg==QUITMSG:
            G_quit =True
        else:
            s.sendall(bytes("{}\r\n".format(usrMsg),"utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    t = Thread(group=None,target=readInput, name="ReadsFromStdin",args=[s])
    t.start()

    while not G_quit:
        data = s.recv(1024)
        print(f"Received {data!r}")
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


#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sel = selectors.DefaultSelector()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #sel.register(s, selectors.EVENT_READ, data=None)
    #sel.register(sys.stdin, selectors.EVENT_READ, data=None)
    t = Thread(group=None,target=readInput, name="ReadsFromStdin",args=[s])
    t.start()

    while not G_quit:
        #events = sel.select(timeout=None)
        data = s.recv(1024)
        print(f"Received {data!r}")

        #for key, mask in events:

            #sock = key.fileobj
            #data = key.data
            #if mask & selectors.EVENT_READ:
            #    print(key.data)
                #recv_data = sock.recv(1024)  # Should be ready to read
        #if to_send == "quit":
        #    quit = True;
        #else:
        #    s.sendall(bytes("{}\r\n".format(to_send),"utf-8"))

"""
design idea: 
- 2 threads, one for user input and one for reading/writing from a socket.
- ncurses for dealing with handling gui interface (in a bit)


"""




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
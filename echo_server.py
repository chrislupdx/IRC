# multiconn-server.py

import sys
import socket
import selectors
import types

conn_list = []
usrID = 0
#example code taken from RealPython socket tutorial
server = Server("Round2ElectricBoogaloo")

def accept_wrapper(sock):
    global usrID
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    conn_list.append([(conn, addr), usrID])
    usrID+=1

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    global usrID
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            print(type(sock))
            #find what user this came from
            messagerID = 0
            for i in range(usrID):
                if conn_list[i][0][0].fileno() == sock.fileno():
                    messagerID = i
            for i in range(usrID):
                messagePreface = "user " + str(messagerID) + " says: "
                conn_list[i][0][0].send(bytes("{}\r\n".format(messagePreface),"utf-8")+ data.outb)
            data.outb = data.outb[sent:] #flush the buffer?

sel = selectors.DefaultSelector()

host, port = sys.argv[1], int(sys.argv[2]) #this list is out of range?
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
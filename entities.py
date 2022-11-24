#example code taken from RealPython socket tutorial
import selectors
import socket
import types

class Server(object):
    def join():
    #client joins a server
        pass

    cmd_list = {    
        'JOIN ': join(),
        'NICK ': 0,
        'LEAVE ': 1
        }
    def __init__(self, name):
        self.name = name
        self.userList = {}
        self.roomList = []
        self.conn_list = [] #temporary
        self.usrID = 0 #temporary
        self.sel = None

    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        self.conn_list.append([(conn, addr), self.usrID])
        self.usrID+=1

    def parseCmd(self, incoming_cmd):
        print("starting parsecmd")
        #compares incoming_cmd to cmd_list, if match returns, calls function with ongoing paramers in incoming_cmd
        #returns false if no recognized command is issued
        print(incoming_cmd)
        #pull apart incoming
        # pass

    def leave():
        print("kicking you out of server")

    def service_connection(self,key, mask):
        sock = key.fileobj
        data = key.data
        #global usrID #this is the second instatitaion of this globally, possibly dangerous?
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
                for i in range(self.usrID):
                    if self.conn_list[i][0][0].fileno() == sock.fileno():
                        messagerID = i
                for i in range(self.usrID):
                    messagePreface = "user " + str(messagerID) + " says: "
                    self.conn_list[i][0][0].send(bytes("{}\r\n".format(messagePreface),"utf-8")+ data.outb)
                self.parseCmd(data.outb) #parses the user commands and executes them
                data.outb = data.outb[sent:] #flush the buffer?

    def startServer(self, host, port): 
        #if we wrap all of this below into a funciton, we still need a way to get argv fed into the wrapper function
        self.sel = selectors.DefaultSelector()
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print(f"Listening on {(host, port)}")
        lsock.setblocking(False)
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
    """
    create a new room object, add it to the room list
    """
    def createRoom(self,roomName):
        newRoom = Room(roomName)
        self.roomList.append(newRoom)

    #returns a 0 for success, -1 for fail
    #todo: can't actually add nicks.  Just do it for ease of testing.
    def addUser(self,fd, sock, nickname = None):
        if fd in userList:
            return -1 #TODO then kick them
        userList[fd] = User(fd, sock, nickname)
 
"""    def listRooms(user):
        return []"""

"""    def doesNickExist(newNick):
        for user in userList:
            if user"""
        
"""
class represents a room on the server
"""        
class Room(object):

    def __init__(self, name):
        self.name = name
        self.userList = []

    def listUsers(self):
        return [u.name for u in self.userList]
            

class User(object):
    #todo: can't actually add nicks.  Just do it for testing.
    def __init__(self, fd, usrSock, nickname = None):
        self.completedHandshake = False
        self.nick = nickname
        self.fd = fd
        self.roomList = [] #can we get around this? idk.
        self.sock = usrSock

    def setNick(self,nickname):
        self.nick = nickname

    """
    def joinRoom(self, roomName):
        #send message to server asking to join room
        self.roomList.append(roomName)
    """
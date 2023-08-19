#example code taken from RealPython socket tutorial
from collections import UserList
import selectors
import socket
import types
from IRCparse import *
from message import *

class Server(object):

    def __init__(self, name):
        self.name = name
        self.userList = {}
        self.roomList = {}
        #self.conn_list = [] #temporary
        self.sel = None
        self.tmpListOfNames = ["Galadriel", "Elrond", "Frodo", "Gilgalad", "Gollum","Morgoth","Turin","Feanor","Legolas","Gimli","Varda","Elwing" ]
        self.tmpID = 0
        #self.cmds = IRCparse.IRCcommands()

    def accept_wrapper(self,sock):
        """
    Accepts a new client connection and sets up I/O for the client.

    This method is responsible for accepting a new client connection and configuring
    I/O for the connection. It registers the connection with the selector, sets it to
    non-blocking mode, and creates a namespace to manage input and output data for
    the connection. The method also adds the newly connected user to the server's
    user list and assigns a temporary username from the `tmpListOfNames`.

    Args:
        sock (socket): The socket object representing the incoming connection.

    Returns:
        None

    Usage:
        self.accept_wrapper(socket_instance)
    """
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        #self.conn_list.append([(conn, addr), self.usrID])
        self.addUser(conn, addr, self.tmpListOfNames[self.tmpID])
        self.tmpID +=1

    def parseCmd(self, incoming_cmd:str, fd):
        """
    Parses and processes an incoming command from a client.

    This method takes an incoming command as a string read from a socket and
    processes it based on the command's content. It converts the incoming command
    into a Message object for easier matching and handles different types of
    user commands, such as connecting to the server, listing rooms, joining/leaving
    rooms, sending messages, and quitting.

    Args:
        //double check incoming is actually string 
        incoming_cmd (str): The incoming command received from the client.
        fd: The file descriptor associated with the client's socket.

    Returns:
        None

    Usage:
        self.parseCmd(incoming_command, file_descriptor)
        """
        #incoming_cmd is string read in through socket
        userMessage = parseUserMessage(incoming_cmd)
        #userMessage is incoming_cmd parsed into a Messege for easy matching
        match userMessage:
            case Connect(host=host, port=port):
                #add user??
                #do we need this case???
                pass
            case ListRooms():
                self.do_listRooms(fd)
            case JoinRoom(roomname=roomname):
                self.do_userJoinRoom(roomname, fd) 
                # what if we returned the value of the thing
            case LeaveRoom(roomname=roomname):
                #remove user from room
                self.do_leaveRoom(roomname, fd)
            case ListRoomUsers(roomname=roomname):
                #send RoomUsersList
                self.do_listRoomUsers(roomname, fd)
            case MessageRoom( roomname=roomname, messageBody=messageBody):
                #send a RoomMessage to every user in every room
                toSend = RoomMessage(self.userList[fd].nick, roomname, messageBody)
                usersRoomList = self.roomList[roomname].userList
                self.do_sendToAllInList(toSend,fd,usersRoomList)
            case MessageUser(recip=recip, messageBody=messageBody):
                toSend = RoomMessage(self.userList[fd].nick, "private message", messageBody)
                recipFD = [i for i in self.userList if self.userList[i].nick == recip][0]
                self.userList[recipFD].sock.send(bytes(str(toSend), 'utf-8'))
            case UserCheckIn():
                #update user time out
                pass
            case Quit():
                #remove user
                self.do_quit(fd)
            case _:
                print(f"found bad message from {fd}: {userMessage}")


    def service_connection(self,key, mask):
        """
    Services a client connection based on the provided key and event mask.

    This method is responsible for servicing a client connection based on the
    provided selector key and the corresponding event mask. It handles both read
    and write events for the client socket. If the event mask includes EVENT_READ,
    the method attempts to receive data from the client socket and processes it.
    If the event mask includes EVENT_WRITE, the method sends any pending data
    and processes incoming commands.

    Args:
        key (selectors.SelectorKey): The selector key associated with the client socket.
        mask (int): The event mask indicating the type of event (read/write).

    Returns:
        None

    Usage:
        self.service_connection(selector_key, event_mask)
    """
        sock = key.fileobj
        data = key.data
        #global usrID #this is the second instatitaion of this globally, possibly dangerous?
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                #remove this fd from the roomlists and the userlist.
                if sock.fileno() in self.userList.keys():
                    self.do_quit(sock.fileno())
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                self.parseCmd(data.outb.decode('utf-8'), sock.fileno())
                data.outb = b'' #flush the buffer?


    def startServer(self, host, port): 
        """
    Starts the chat server and listens for incoming connections.

    This method initializes the server, binds it to the specified host and port,
    and begins listening for incoming connections. It utilizes the selectors module
    to manage I/O events on multiple sockets, enabling efficient handling of multiple
    client connections. The method enters a loop where it waits for and processes
    events such as accepting new connections and servicing existing connections.
    The server continues to run until a keyboard interrupt (Ctrl+C) is caught.

    Args:
        host (str): The host address on which the server will listen.
        port (int): The port number on which the server will listen.

    Returns:
        None

    Usage:
        self.startServer(host, port)
    """
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
                events = self.sel.select(timeout=3)
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


    def do_userJoinRoom(self, roomName, fd):
        if roomName not in self.roomList.keys():
            print("creating room " + roomName)
            self.createRoom(roomName)
        (self.roomList[roomName]).addUsertoRoom(fd)
        print("adding user " + self.userList[fd].nick +" to " +roomName)
        self.do_messageRoom(RoomMessage(self.name, roomName, f"{self.userList[fd].nick} has joined {roomName}"), fd)

    #sends a messagge to all users in the room from user at fd
    def do_messageRoom(self, message,fd):
        match message:
            case RoomMessage():
                usersRoomList = self.roomList[message.roomname].userList
                print(str(message))
                self.do_sendToAllInList(message,fd,usersRoomList)
            case _:
                raise Exception("recieved invalid message in do_messageRoom: " + str(message))

    #creates a new room and adds it to list
    def createRoom(self,roomName):
        newRoom = Room(roomName)
        self.roomList[roomName] = newRoom

    #returns a 0 for success, -1 for fail
    #todo: can't actually add nicks.  Just do it for ease of testing.
    def addUser(self,sock, addr,nickname = None):
        fd = sock.fileno()
        if fd in self.userList:
            return -1 #TODO then kick them
        self.userList[fd] = User(fd, sock, addr, nickname)

    #sends message to all users in list
    def do_sendToAllInList(self,message, fd, userList):
        for fd in userList:
            sent = self.userList[fd].sock.send(bytes(str(message), 'utf-8'))
        return sent

    def do_quit(self, fd):
        print(f"kicking {fd} out of server")
        for room in self.roomList:
            if fd in self.roomList[room].userList: self.roomList[room].userList.remove(fd)
        del self.userList[fd]

    def do_listRooms(self, fd):
        print(f'sent list of rooms to {fd}')
        msg = RoomList([self.roomList[room].name for room in self.roomList])
        self.userList[fd].sock.send(bytes(str(msg), 'utf-8'))

    def do_leaveRoom(self, roomtoleave, fd):
        print("leavingRoom:", roomtoleave)
        self.roomList[roomtoleave].userList.remove(fd)
        

    def do_listRoomUsers(self, roomToList, fd):
        print(f'sending list of users in {roomToList} to {fd}')
        #should be nickname??
        msg = RoomUsersList([self.userList[user].nick for user in self.roomList[roomToList].userList])
        self.userList[fd].sock.send(bytes(str(msg), 'utf-8'))

"""
class represents a room on the server
"""        
class Room(object):

    def __init__(self, name):
        self.name = name
        self.userList = []

    def addUsertoRoom(self,fd):
        if fd not in self.userList:
            self.userList.append(fd)

class User(object):
    #todo: can't actually add nicks.  Just do it for testing.
    def __init__(self, fd, usrSock, addr, nickname = None):
        self.completedHandshake = False
        self.nick = nickname
        self.fd = fd
        self.addr = addr
        self.roomList = [] #can we get around this? idk.
        self.sock = usrSock

    def setNick(self,nickname):
        self.nick = nickname


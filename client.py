import socket
from time import sleep
import selectors
import sys
from threading import Thread
from IRCparse import *
import select

HOST, PORT = sys.argv[1], int(sys.argv[2])

class Client():

    def __init__(self, host, port):
        """
        Initializes a new Client instance.

        Args:
            host (str): The hostname or IP address of the chat server.
            port (int): The port number to connect to on the chat server.
        """
        self.host = host
        self.port = port
        self.curRoom = None
        self.G_quit = False
        self.rooms = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.setblocking(False)
    
    def readSocket(self, s:socket):
        """
    Reads data from a socket and processes server messages.

    This method reads data from a socket and processes server messages
    received from the chat server. It runs in a loop until the client
    sets the `G_quit` flag to True.

    Args:
        s (socket): The socket object to read data from.

    Returns:
        None

    Raises:
        OSError: If there is an issue with the socket operation.

    Usage:
            client.readSocket(socket_instance)
    """
        self.s.setblocking(0)
        while not self.G_quit:
            #data = self.s.recv(1024)
            self.s.setblocking(0)
            ready = select.select([self.s], [], [], 1)
            if ready[0]:
                data = self.s.recv(4096)
                if data==b'':
                    print("Server disconnected.")
                    self.G_quit = True
                    return
                serverMsg = self.parseServerMessage(data.decode('utf-8'))
                self.executeServerMessage(serverMsg)   

    # def run(self):
    #     """
    #     Connects to the chat server and starts the client's main loop.

    #     This method establishes a connection to the chat server using the provided
    #     host and port. It then spawns two threads: one for reading user input
    #     from the standard input and another for reading server messages from
    #     the socket. The client's main loop runs until the `G_quit` flag is set
    #     to True, at which point the client terminates.

    #     Returns:
    #         None

    #     Usage:
    #         client.run()
    #     """
    #     self.s.connect((self.host, self.port))
    #     #self.s.bind((self.host, self.port))
    #     #self.s.listen(1)
    #     #conn, addr = self.s.accept()
    #     t = Thread(group=None,target=client.readInput, name="ReadsFromStdin",args=[self.s])
    #     t.start()      
    #     s = Thread(group=None,target=client.readSocket, name="ReadsFromSocket",args=[self.s])
    #     s.start()
    #     while not self.G_quit:
    #         sleep(.1)
    #     sys.exit()
    
    def run(self):
            """
            Connects to the chat server and starts the client's main loop.

            This method establishes a connection to the chat server using the provided
            host and port. It then spawns two threads: one for reading user input
            from the standard input and another for reading server messages from
            the socket. The client's main loop runs until the `G_quit` flag is set
            to True, at which point the client terminates.

            Returns:
                int: Exit code (0 for successful execution, 1 for an error).

            Usage:
                exit_code = client.run()
            """
            try:
                self.s.connect((self.host, self.port))
                t = Thread(group=None, target=self.readInput, name="ReadsFromStdin", args=[self.s])
                t.start()
                s = Thread(group=None, target=self.readSocket, name="ReadsFromSocket", args=[self.s])
                s.start()
                while not self.G_quit:
                    sleep(0.1)
                return 0
            except Exception as e:
                print("An error occurred:", str(e))
                return 1

    
    def parseUserCommand(self, entry:str) -> Message:
        """
    Parses a user's input entry and converts it into a corresponding Message object.

    This method takes a user's input entry and processes it to create an appropriate
    Message object that represents the user's command for the chat client. The method
    recognizes various commands, such as connecting to a server, listing rooms,
    joining/leaving rooms, sending messages to rooms or individual users, and quitting.

    Args:
        entry (str): The user's input command entry.

    Returns:
        Message: A Message object representing the parsed user command.

    Usage:
        command = client.parseUserCommand(input_entry)
        """
        cmd = entry.split(' ')[0]
        match cmd:
            #user typed "/connect HOST PORT"
            case "/connect":
                host = entry.split(' ')[1]
                port = entry.split(' ')[2]
                return Connect(host, port)
            #user typed "/listrooms"
            case "/listrooms":
                return ListRooms()
            #user typed "/join roomname"
            case "/join":
                roomname = entry.split(' ')[1]
                return JoinRoom(roomname=roomname)
            #user typed "/leave roomname"
            case "/leave":
                roomname = entry.split(' ')[1]
                return LeaveRoom(roomname)
            #user typed "/list roomname"
            case "/list":
                roomname = entry.split(' ')[1]
                return ListRoomUsers(roomname)
            #usertyped "/msg messagebody"
            case "/msg":
                message = ' '.join(entry.split(' ')[1:])
                return MessageRoom(self.curRoom, message)
            #user typed "/msgroom #roomname : messageBody"
            case "/msgroom":
                roomname = entry.split(' ')[1][1:] #get roomname without '#'
                message = entry.split(':')[1].strip()
                return MessageRoom(roomname, message)
            #user typed "/dm recip : messagebody"
            case "/dm":
                recip = entry.split(' ')[1]
                message = entry.split(':')[1]
                return MessageUser(recip, message)
            case "/quit":
                return Quit()
        
    def parseServerMessage(self, serverMessage:str) -> Message:
        """
        Parses a server message and converts it into a corresponding Message object.

        This method takes a server message received from the chat server and processes
        it to create an appropriate Message object that represents the server's response
        or broadcast. The method recognizes different types of server messages, such as
        room lists, user lists, room messages, check-in notifications, and default messages.

        Args:
            serverMessage (str): The server message received from the chat server.

        Returns:
            Message: A Message object representing the parsed server message.

        Usage:
            message = client.parseServerMessage(server_response)
        """
        header = serverMessage.split(' ')[0]
        match header:
            case "ROOMLIST":
                roomlist = [room for room in serverMessage.split(' ')[1:]]
                return RoomList(roomlist)
            case "ROOMUSERLIST":
                roomusers = [user for user in serverMessage.split(' ')[1:]]
                return RoomUsersList(roomusers)
            case "ROOMMESSAGE":
                sender = serverMessage.split(' ')[1].split(":")[0]
                roomname = serverMessage.split(' ')[1].split(':')[1]
                messageBody = serverMessage.split(':')[2].strip()
                return RoomMessage(sender, roomname, messageBody)
            case "CHECKIN":
                return ServerCheckin()
            case _:
                return RoomMessage("SERVER ", serverMessage)
        
    def executeServerMessage(self, serverMsg):
        """
    Executes actions based on the received server message.

    This method takes a parsed server message and performs appropriate actions
    based on the content of the message. It handles different types of server
    messages, such as displaying room lists, showing room users, printing room messages,
    and handling server check-ins.

    Args:
        serverMsg: A parsed server message as a Message object.

    Returns:
        None

    Raises:
        Exception: If an invalid server message is received.

    Usage:
        client.executeServerMessage(server_message)
    """
        match serverMsg:
            case RoomList(roomlist=roomlist):
                print("Available Rooms: ")
                for room in roomlist: print(room)
            case RoomUsersList(roomusers=roomusers):
                print("Users in room: ")
                for user in roomusers: print(user)
            case RoomMessage(sender=sender, roomname=roomname, messageBody=messageBody):
                print(f"message from {roomname}")
                print(sender + ": " + messageBody)
            case ServerCheckin():
                pass
            case _:
                raise Exception("execute server message recieved invalid server message: " + str(serverMsg))

    def readInput(self, s:socket):
        """
    Reads user input and processes user commands for the chat client.

    This method continuously reads user input from the standard input and processes
    the user's commands. It handles various user commands, such as connecting to
    the server, listing rooms, joining/leaving rooms, sending messages, and quitting
    the client. The method interacts with the chat server by sending appropriate
    requests based on the parsed user commands.

    Args:
        s (socket): The socket object used for communication with the chat server.

    Returns:
        None

    Usage:
        client.readInput(socket_instance)
    """
        while not self.G_quit:
            usrMsg = input()
            parsedCmd = self.parseUserCommand(usrMsg)
            match parsedCmd:
                case Connect(host=host, port=port):
                    pass
                case ListRooms():
                    #send request to server
                    s.sendall(bytes(str(parsedCmd), 'utf-8'))
                case JoinRoom(roomname=roomname):
                    #send request to server
                    s.sendall(bytes(str(parsedCmd), 'utf-8'))
                    self.curRoom = roomname
                    self.rooms += [roomname]
                case LeaveRoom(roomname=roomname):
                    if roomname not in self.rooms:
                        print("cannot leave room, not in room")
                        continue
                    #send request to server
                    s.sendall(bytes(str(parsedCmd), 'utf-8'))
                    #wait for server response
                case ListRoomUsers(roomname=roomname):
                    #send request to server
                    s.sendall(bytes(str(parsedCmd), 'utf-8'))
                case MessageRoom(roomname=roomname, messageBody=message):
                    #send request to server
                    s.sendall(bytes(str(parsedCmd), 'utf-8'))
                case MessageUser(recip=recip, messageBody=messageBody):
                    s.sendall(bytes(str(parsedCmd), 'utf-8'))
                case Quit():
                    #send request to server
                    print("quitting....")
                    s.sendall(bytes(str(parsedCmd), 'utf-8'))
                    self.G_quit = True

                case _:
                    #error in user command, send nothing, reprompt
                    print("invalid user command")
                    continue

if __name__ == '__main__':
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    client = Client(HOST, PORT)
    client.run()

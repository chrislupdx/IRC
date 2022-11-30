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
        self.host = host
        self.port = port
        self.curRoom = None
        self.G_quit = False
        self.rooms = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.setblocking(False)
    
    def readSocket(self, s:socket):
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

    def run(self):
        self.s.connect((self.host, self.port))
        #self.s.bind((self.host, self.port))
        #self.s.listen(1)
        #conn, addr = self.s.accept()
        t = Thread(group=None,target=client.readInput, name="ReadsFromStdin",args=[self.s])
        t.start()      
        s = Thread(group=None,target=client.readSocket, name="ReadsFromSocket",args=[self.s])
        s.start()
        while not self.G_quit:
            sleep(.1)
        sys.exit()
    
    def parseUserCommand(self, entry:str) -> Message:
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
                print(f"found a join message, body: {roomname}")
                print(f"message as string: {JoinRoom(roomname=roomname)}")
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
            case "/quit":
                return Quit()
        
    def parseServerMessage(self, serverMessage:str) -> Message:
        header = serverMessage.split(' ')[0]
        match header:
            # case "CONNECTACK":
            #     return ConnectAck
            case "ROOMLIST":
                roomlist = [room for room in serverMessage.split(' ')[1:]]
                return RoomList(roomlist)
            # case "JOINROOMACK":
            #     roomname = serverMessage.split(' ')[1]
            #     return JoinRoomAck(roomname)
            # case "LEAVEROOMACK":
            #     return LeaveRoomAck()
            case "ROOMUSERLIST":
                roomusers = [user for user in serverMessage.split(' ')[1:]]
                return RoomUsersList(roomusers)
            case "ROOMMESSAGE":
                roomname = serverMessage.split(' ')[1]
                messageBody = serverMessage.split(':')[1].strip()
                return RoomMessage(roomname, messageBody)
            # case "MESSAGEACK":
            #     return MessageAck()
            case "CHECKIN":
                return ServerCheckin()
            # case "QUITACK":
            #     return QuitAck()
            case _:
                return RoomMessage("SERVER ", serverMessage)
        
    def executeServerMessage(self, serverMsg):
        match serverMsg:
            case RoomList(roomlist=roomlist):
                print("Available Rooms: ")
                for room in roomlist: print(room)
            case RoomUsersList(roomlist=roomusers):
                print("Users in room: ")
                for user in roomusers: print(user)
            case RoomMessage(roomname=roomname, messageBody=messageBody):
                print(roomname+": ", end='')
                print(messageBody)
            case ServerCheckin():
                pass
            case _:
                raise Exception("execute server message recieved invalid server message: " + str(serverMsg))

    def readInput(self, s:socket):
        while not self.G_quit:
            usrMsg = input()
            if usrMsg[0]!="/":
                #they are just typing into whatever chat window they had last
                #TODO: have the client keep track of this
                if self.curRoom != "":
                    s.sendall(bytes("{} {} {}\r\n".format('ROOMMSG', self.curRoom, usrMsg),"utf-8"))
                else:
                    s.sendall(bytes("{} {}\r\n".format('DEFAULT', usrMsg),"utf-8"))
                if usrMsg == "quit":
                    self.G_quit = True
            else:
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
                        """
                        #wait for server response
                        reply = self.getReply()
                        match reply:
                            case RoomUsersList(roomusers):
                                #print list of users in room
                                for user in roomusers: print(user)
                            case _:
                                raise Exception("recieved invalid server reply to LeaveRoom: " + str(reply))
                        """
                    case MessageRoom(roomname=roomname, messageBody=message):
                        #send request to server
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        """
                        reply = self.getReply()
                        match reply:
                            case MessageAck():
                                #message was sent
                                continue
                            case _:
                                raise Exception("received invalid server reply to MessageRoom: " + str(reply))
                        """
                    case Quit():
                        #send request to server
                        print("quitting....")
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        self.G_quit = True

                    case _:
                        #error in user command, send nothing, reprompt
                        raise Exception("invalid command entered: " + usrMsg)

"""
G_quit = False
cmds = IRCcommands()
curRoom = ""
def readInput(s:socket):
    global G_quit
    global cmds
    global curRoom
    while not G_quit:
        usrMsg = input()
        if usrMsg[0]!="/":
            #they are just typing into whatever chat window they had last
            #TODO: have the client keep track of this
            if curRoom != "":
                s.sendall(bytes("{} {} {}\r\n".format('ROOMMSG', curRoom, usrMsg),"utf-8"))
            else:
                s.sendall(bytes("{} {}\r\n".format('DEFAULT', usrMsg),"utf-8"))
        else:
            #we have a command, parse it!
            cmd, payload = parse(usrMsg)
            if cmd == cmds.joinUSR:
                s.sendall(bytes("{} {}\r\n".format(cmds.JOINROOM,payload),"utf-8"))
                curRoom = payload.split()[0]
            if cmd == cmds.quitUSR:
                #TODO: send disconnect request to server.
                G_quit =True
            if cmd in IRCcommands.messagetypes:
                args = None
                splitmsg = usrMsg.split()
                withoutfirst = splitmsg[1:]
                if len(withoutfirst) > 1:
                    args = withoutfirst
                s.sendall(bytes("SERVERFUNCTION {}, body {} \r\n".format(cmd, args),"utf-8"))
"""

if __name__ == '__main__':
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    client = Client(HOST, PORT)
    client.run()
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        t = Thread(group=None,target=client.readInput, name="ReadsFromStdin",args=[s])
        t.start()

        while not client.G_quit:
            data = s.recv(1024)
            to_print = data.decode("utf-8")
            print(to_print)
    """
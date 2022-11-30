import socket
from time import sleep
import selectors
import sys
from threading import Thread
from IRCparse import *

HOST, PORT = sys.argv[1], int(sys.argv[2])

class Client():

    def __init__(self):
        self.curRoom = None
        self.G_quit = False
        self.rooms = []
    
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
                return JoinRoom(roomname)
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
                message = entry.split(' ')[1]
                return MessageRoom(self.curRoom, message)
            #user typed "/msgroom #roomname : messageBody"
            case "/msgroom":
                roomname = entry.split(' ')[1][1:] #get roomname without '#'
                message = entry.split(':')[1].strip()
                return MessageRoom(roomname, message)
            case "/quit":
                return Quit()
    
    def readInput(self, s:socket):
        while not G_quit:
            usrMsg = input()
            if usrMsg[0]!="/":
                #they are just typing into whatever chat window they had last
                #TODO: have the client keep track of this
                if self.curRoom != "":
                    s.sendall(bytes("{} {} {}\r\n".format('ROOMMSG', self.curRoom, usrMsg),"utf-8"))
                else:
                    s.sendall(bytes("{} {}\r\n".format('DEFAULT', usrMsg),"utf-8"))
            else:
                parsedCmd = parseUserCommand(usrMsg)
                match parsedCmd:
                    case Connect(host, port):
                        pass
                    case ListRooms():
                        #send request to server
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        #wait for server response
                        #print list of rooms
                    case JoinRoom(roomname):
                        #send request to server
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        #wait for server ack
                        #add room to list of joined rooms
                        self.rooms += [roomname]
                        self.curRoom = roomname
                    case LeaveRoom(roomname):
                        #send request to server
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        #wait for server response
                        #remove room from list of joined rooms
                    case ListRoomUsers(roomname):
                        #send request to server
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        #wait for server response
                        #print list of users in room
                    case MessageRoom(roomname, message):
                        #send request to server
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        #wait for ack
                    case Quit():
                        #send request to server
                        s.sendall(bytes(str(parsedCmd), 'utf-8'))
                        #wait for server ack
                        #disconnect from server
                        G_quit = True
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
    client = Client()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        t = Thread(group=None,target=client.readInput, name="ReadsFromStdin",args=[s])
        t.start()

        while not client.G_quit:
            data = s.recv(1024)
            to_print = data.decode("utf-8")
            print(to_print)
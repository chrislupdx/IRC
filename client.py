import socket
from time import sleep
import selectors
import sys
from threading import Thread
from IRCparse import *

HOST, PORT = sys.argv[1], int(sys.argv[2])

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
            parsedCmd = parseUserCommand(usrMsg)
            match parsedCmd:
                case Connect(host, port):
                    pass
                case ListRooms():
                    pass
                case JoinRoom(roomname):
                    pass
                case LeaveRoom(roomname):
                    pass
                case ListRoomUsers(roomname):
                    pass
                case MessageRoom(roomnames, message):
                    pass
                case Quit():
                    pass
                case _:
                    raise Exception("invalid command entered: " + usrMsg)
            """
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    t = Thread(group=None,target=readInput, name="ReadsFromStdin",args=[s])
    t.start()

    while not G_quit:
        data = s.recv(1024)
        to_print = data.decode("utf-8")
        print(to_print)
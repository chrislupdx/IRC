from unittest.mock import MagicMock, call, PropertyMock
from server import server
#you can't do all of them so do like an example of one root->wing

def test_parse_cmd():
    #parsecmd takes a string, thre are 10 cases to test for lol
    pass

def test_accept_wrapper():
    # takes a socket 
    #currently doesn't return anything of value?
    pass

def service_connection():
    #type hitns for key and mask inputs coud be dope
    #there's no return
    pass

def test_startServer():
    #no return alue
    #takes host and port
    pass

def test_do_userJoinRoom():
    # also no return values
    pass

def test_domessageRoom():
    #takes an fd, messsage
    #returns nothing yet
    pass

def test_createRoom():
    # takes a roomName
    #has not return value
    pass

def test_addUser():
    #no return
    #takes a socket, address, nickname
    pass

def test_do_sendToAllInList():
    #takes message, fd, userlist
    #returns sent!
    pass

def test_do_quit():
    #tagkes fd
    pass

def test_do_listRooms():
    #takes fd
    #returns nothing
    pass

def test_do_leaveRoom():
    #takes fd
    # returns nothing
    pass

def test_do_listRoomUsers():
    #no return
    #takes fd, roomtolist
    pass
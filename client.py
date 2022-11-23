#this is client
from socket import *

class client():
    def __init__(self):
        self.name = "servername"
        self.port =  12000

    def connect(socket, port, domain):
        '''
        attempts to connect to a client irc room with the socket, port, and domain information
        '''
        print('connect has been called')


    #exit
    def request_disconnect():
        '''
        if we are in a paradigm where the server is the one with the
         ability to disconnect clients, this is the function for the client to 
         execute a disconnect from an IRC server
         -returns false if something happens strange
        '''
        pass

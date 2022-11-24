class Server(object):
    def __init__(self, name):
        self.name = name
        self.userList = {}
        self.roomList = []

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
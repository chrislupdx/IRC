class Server(object):

    def __init__(self, name):
        self.name = name
        self.userList = []
        self.roomList = []

    """
    create a new room object, add it to the room list
    """
    def createRoom(roomName):
        newRoom = Room(roomName)
        self.roomList.append(newRoom)

    def listRooms(user):
        return []
        
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

    def __init__(self, nickname, address):
        self.nickname = nickname
        self.address = address
        self.roomList = []
    
    def joinRoom(self, roomName):
        #send message to server asking to join room
        self.roomList.append(roomName)
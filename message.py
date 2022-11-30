class Message:

    def __init__(self, header:str='', body:str=''):
        self.header = header
        self.body = body

    def __str__(self):
        return self.header + " " + self.body + "\r\n"
    
    def displayMessagetext(self):
        print('header is', header)
        print('body is ', body)
    
class UserMessage(Message):
    def __init__(self, header, body):
        super().__init__(header, body)
    
class Connect(UserMessage):
    def __init__(self, host:str, port:str):
        super().__init__(None, host+port)

class ListRooms(UserMessage):
    def __init__(self):
        super().__init__("LISTROOMS")

class JoinRoom(UserMessage):
    def __init__(self, roomname):
        self.roomname = roomname
        super().__init__("JOINROOM", roomname)

class LeaveRoom(UserMessage):
    def __init__(self, roomname):
        self.roomname = roomname
        super().__init__("LEAVEROOM", roomname)

class ListRoomUsers(UserMessage):
    def __init__(self, roomname):
        self.roomname = roomname
        super().__init__("LISTROOMUSERS", roomname)

class MessageRoom(UserMessage):
    def __init__(self, roomname, messageBody):
        self.messageBody = messageBody
        self.roomname = roomname
        body = '#roomname : ' + messageBody
        super().__init__("MESSAGEROOM", body)

class UserCheckIn(UserMessage):
    def __init__(self):
        super().__init__("CHECKIN")

class Quit(UserMessage):
    def __init__(self):
        super().__init__("QUIT")

"""
Server Messages:
    - ConnectAck: sent by server to client after receiving and completing JoinRoom from client
    - RoomList: sent by server to client after recieving ListRooms
    - 
"""

class ServerMessage(Message):
    def __init__(self, header, body):
        super().__init__(header, body)

"""
class ConnectAck(ServerMessage):
    def __init__(self):
        super().__init__("CONNECTACK")
"""

class RoomList(ServerMessage):
    def __init__(self, roomlist):
        self.roomlist = roomlist
        body = ''
        for room in roomlist: body += room+' '
        super().init("ROOMLIST", body)

"""
class JoinRoomAck(ServerMessage):
    def __init__(self, roomname):
        super().__init__("JOINROOMACK", roomname)
"""

"""
class LeaveRoomAck(ServerMessage):
    def __init__(self, roomname):
        super().__init__("LEAVEROOMACK", roomname)
"""

class RoomUsersList(ServerMessage):
    def __init__(self, roomusers):
        body=''
        for roomuser in roomusers: body += roomuser+' '
        super().__init__("ROOMUSERLIST", body)

class RoomMessage(ServerMessage):
    def __init__(self, roomname, messageBody):
        self.roomname = roomname
        self.messageBody = messageBody
        body = roomname + ':' + messageBody
        super().__init__("ROOMMESSAGE", body)

"""
class MessageAck(ServerMessage):
    def __init__(self):
        super().__init__("MESSAGEACK")
"""

class ServerCheckin(ServerMessage):
    def __init__(self):
        super().__init__("CHECKIN")

"""
class QuitAck(ServerMessage):
    def __init__(self):
        super().__init__("QUITACK")
"""
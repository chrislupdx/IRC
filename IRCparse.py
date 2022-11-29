from message import *
#used for client parsing.  Maybe it will be useful for server parsing, too
class IRCcommands(object):
	messagetypes = ['/joinroom', '/leaveroom', '/listrooms' ]

	def __init__(self):
		# what the server reads.  Every message needs to
		# have one of these when sendign to the server.

		self.JOINROOM = "JOIN" 
		self.LEAVE = "LEAVE"
		self.DEFAULT = "DEFAULT" #TODO: for developing		
		self.MSGROOM = "ROOMMSG" #followed by roomname and then the entire message

		#what the user types
		self.joinUSR = "/join" #connects them to the server??
		self.quitUSR = "/quit" #disconnects them from the server??

	# msttypeDict = {
	# 	'JOINROOM' : joinRoom,
	# 	'LEAVEROOM' : leaveRoom,
	# }
"""
returns a tuple of parsed command in format:
(type,payload)

Note that all trailing and leading space information 
(carriage returns, etc) are removed.
"""
"""
def parse(unparsed):
	cleaned = unparsed.strip()
	cmd = unparsed.split()[0]
	payload = " ".join(unparsed.split()[1:]).rstrip()
	return cmd, payload
"""

def parseUserCommand(entry:str) -> Message:
	cmd = entry.split(' ')[0]
	match cmd:
		case "/connect":
			host = entry.split(' ')[1]
			port = entry.split(' ')[2]
			return Connect(host, port)
		case "/listrooms":
			return ListRooms()
		case "/join":
			roomname = entry.split(' ')[1]
			return JoinRoom(roomname)
		case "/leave":
			roomname = entry.split(' ')[1]
			return LeaveRoom(roomname)
		case "/list":
			roomname = entry.split(' ')[1]
			return ListRoomUsers(roomname)
		case "/msg":
			roomnames = [roomname[1:] for roomname in entry.split(' ') if roomname[0]=="#"]
			message = entry.split(":")[1]
			return MessageRoom(roomnames, message)
		case "/quit":
			return Quit()

def parseUserMessage(unparsedMsg:str) -> Message:
	clean = unparsedMsg.strip()
	header = clean.split(' ')[0]
	match header:
		case "LISTROOMS":
			return ListRooms()
		case "JOINROOM":
			return JoinRoom(clean.split(' ')[1])
		case "LEAVEROOM":
			return LeaveRoom(clean.split(' ')[1])
		case "LISTROOMUSERS":
			return ListRoomUsers(clean.split(' ')[1])
		case "MESSAGE":
			body = clean.split(' ')
			roomnames = [roomname[1:] for roomname in body if roomname[0] == "#"] 
			return MessageRoom(roomnames, body.split(":")[1])
		case "CHECKIN":
			return UserCheckIn()
		case "QUIT":
			return Quit()

def parseServerMessage(unparsedMsg:str) -> Message:
	clean = unparsedMsg.strip()
	header = clean.split(' ')[0]
	match header:
		case "CONNECTACK":
			return ConnectAck()
		case "ROOMLIST":
			roomlist = [room for room in clean.split(' ')[1:]]
			return RoomList(roomlist)
		case "JOINROOMACK":
			return JoinRoomAck()
		case "LEAVEROOMACK":
			return LeaveRoomAck()
		case "ROOMUSERLIST":
			roomusers = [user for user in clean.split(' ')[1:]]
			return RoomUsersList(roomusers)
		case "MESSAGEACK":
			return MessageAck()
		case "QUIACK":
			return QuitAck()
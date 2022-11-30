from message import *

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
		case "MESSAGEROOM":
			roomname = clean.split(' ')[1][1:]
			messageBody = clean.split(':')[1].strip()
			print("found MESSAGE from client")
			print("roomname: " + roomname)
			print("messageBody: " + messageBody)
			return MessageRoom(roomname, messageBody)
		case "CHECKIN":
			return UserCheckIn()
		case "QUIT":
			return Quit()

def parseServerMessage(unparsedMsg:str) -> Message:
	clean = unparsedMsg.strip()
	header = clean.split(' ')[0]
	match header:
		case "ROOMLIST":
			roomlist = [room for room in clean.split(' ')[1:]]
			return RoomList(roomlist)
		case "ROOMUSERLIST":
			roomusers = [user for user in clean.split(' ')[1:]]
			return RoomUsersList(roomusers)
		case "ROOMMESSAGE":
			roomname = clean.split(' ')[1]
			messageBody = clean.split(':')[1]
			return RoomMessage(roomname, messageBody)
		case "QUIACK":
			return QuitAck()
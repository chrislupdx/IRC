# List Of Resources

## IRC
- original rfc: https://www.rfc-editor.org/rfc/rfc1459#section-4.6.4
- capability notification for "real" servers: https://ircv3.net/specs/extensions/capability-negotiation


## Python:
- socket programming: https://realpython.com/python-sockets/
- regex: https://www.guru99.com/python-regular-expressions-complete-tutorial.html

# Usage

## Init: 
- Server: In a terminal window:
> python echo_server.py HOST PORT

- Client: In a separate terminal window:
> python echo_client.py HOST PORT

# Connecting:

# Client Commands:
/listrooms - client sends ListRooms() message
/join roomname - client sends JoinRoom(roomname) message
/leave roomname - cliend sends LeaveRoom(roomname)
/list roomname - client sends ListRoomUsers()
/msg messagebody - client sends MessageRoom(curRoom, messageBody)
/msgroom #roomname : messageBody - client sends MessageRoom(roomname, messageBody)
/quit

/leaveroom [roomname]
/joinroom [roomname]
/listrooms

# Todo
- Create usernames
- 

# Developer Tips
- 

cmd_list = {    
#'JOIN ': join(),
'NICK ': 0,
'LEAVE ': 1
}

#used for client parsing.  Maybe it will be useful for server parsing, too
class IRCcommands(object):
	def __init__(self):
		# what the server reads.  Every message needs to
		# have one of these when sendign to the server.
		self.JOIN="JOIN"
		self.NICK="NICK"
		self.DEFAULT = "DEFAULT" #TODO: for developing

		#what the user types
		self.joinUSR = "/join"
		self.quitUSR = "/quit"

"""
returns a tuple of parsed command in format:
(type,payload)

Note that all trailing and leading space information 
(carriage returns, etc) are removed.
"""
def parse(unparsed):
	cmd = unparsed.split()[0]
	payload = " ".join(unparsed.split()[1:]).rstrip()
	return cmd, payload






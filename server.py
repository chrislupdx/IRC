import sys
import entities

host, port = sys.argv[1], int(sys.argv[2])
server = entities.Server("Round2ElectricBoogaloo")
server.startServer(host,port)
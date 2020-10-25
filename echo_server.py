# echo server.py
import socket
import time

# create a socket object
# The arguments passed to socket() specify the address family and
# socket type. AF_INET is the Internet address family for IPv4.
# SOCK_STREAM is the socket type for TCP,
# the protocol that will be used to transport our messages in the network.


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostbyname('localhost')

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

print("starting the server....")
while True:
    # establish a connection
    # accept() blocks and waits for an incoming connection.
    # When a client connects, it returns a new socket object representing the connection
    # and a tuple holding the address of the client.
    # The tuple will contain (host, port) for IPv4 connections
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode('ascii'))
    clientsocket.close()

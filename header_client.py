import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# these are acutally the ip address and port of the server
hostname = socket.gethostbyname('localhost')
port = 1234

s.connect((hostname, port))

fullMsg = ''
newMessage = True

while True:
    msg = s.recv(16)

    # to process info in case there is a new message
    if newMessage:
        print("header => ", msg[:HEADERSIZE])
        msglen = int(msg[:HEADERSIZE])
        newMessage = False
        print(f"length of new message is {msglen}")

    fullMsg += msg.decode()

    # resetting things if one complete message has been sent
    if len(fullMsg) == msglen + HEADERSIZE:
        print('full message recieved')
        print(fullMsg[HEADERSIZE:])
        newMessage = True
        fullMsg = ''

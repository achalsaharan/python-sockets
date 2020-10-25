import socket
import selectors

host = socket.gethostbyname('localhost')
port = 9999
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f'listening on {host} : {port} ....')
lsock.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(lsock, selectors.EVENT_READ, data=None)

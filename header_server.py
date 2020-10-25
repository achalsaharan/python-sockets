import socket
import time

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostbyname('localhost')
port = 1234
s.bind((hostname, port))
s.listen(5)

print(f"staring server on {hostname}:{port}")

while True:
    clientSocket, address = s.accept()
    print(f'Got a connection from {address}')

    while True:
        time.sleep(3)
        msg = f"The time is {time.time()}"
        response = f"{len(msg):<{HEADERSIZE}}" + msg
        print(response)

        clientSocket.send(response.encode())

        print('Done sending the message...\n***********\n')

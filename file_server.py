# file server
import socket
from checkUpdate import updateChecker

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname('localhost')
port = 9000

serversocket.bind((host, port))

serversocket.listen(5)

print(f"server listening on {port}")

while True:
    conn, addr = serversocket.accept()
    print(f'got a connection from {addr}')

    clientNo = conn.recv(1024).decode()
    filename = updateChecker(clientNo)

    # close connection if there is no file to be sent
    if filename == 0:
        conn.send('no-file'.encode())
        conn.close()
        continue

    # send file

    # first send filename to the client
    conn.send(filename.encode())

    filename = './serverFiles/'+filename
    f = open(filename, 'rb')

    # sending the actual file to the client
    l = f.read(1024)
    while(l):
        conn.send(l)
        print(f'sent {repr(l)}')
        l = f.read(1024)

    f.close()

    print('done sending')
    conn.close()

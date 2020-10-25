# file client
import socket

clientNo = '2'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname('localhost')
port = 9000

s.connect((host, port))
s.send(clientNo.encode())

filename = s.recv(12).decode()
print(f'*** {filename} *****')
if filename == 'no-file':
    print('no file to download')

filename = './clientFiles/' + filename

# 'wb' means
# w -> open in write mode
# b -> means we will be wiritng binary data to the file


with open(filename, 'wb') as f:
    print('file opened')
    print('recieving data')
    while True:
        data = s.recv(1024)
        print(data.decode())

        if not data:
            break

        # write data to the file
        f.write(data)

print('recieved the file')
s.close()
print('connection closed')

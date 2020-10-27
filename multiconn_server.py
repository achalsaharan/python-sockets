import socket
import selectors
import types

host = socket.gethostbyname('localhost')
port = 9999
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f'listening on {host} : {port} ....')
lsock.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(lsock, selectors.EVENT_READ, data=None)


def acceptWrapper(sock):
    conn, addr = sock.accept()
    print("accepted connection from ", addr)
    conn.setblocking(False)

    # what is the use of this?
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data)


def serviceConnection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to ", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("echoing", repr(data.outb), " to ", data.addr)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data == None:
                acceptWrapper(key.fileobj)
            else:
                serviceConnection(key, mask)

except KeyboardInterrupt:
    print('caught keyboard interrupt, exiting...')

finally:
    sel.close()

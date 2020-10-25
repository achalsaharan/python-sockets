import socket
import select

HEADER_LENGTH = 10

hostname = socket.gethostbyname('localhost')
port = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((hostname, port))
server_socket.listen()

sockets_list = [server_socket]
clients = {}

print(f"server listening on {hostname} : {port} ....")


def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {
            'header': message_header,
            'data': client_socket.recv(message_length)
        }

    except:
        return False


while True:

    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    # iterate over notified sockets

    for notified_socket in read_sockets:

        # if the notifed socket is the server socket that means its a new connection
        if notified_socket == server_socket:

            # accept the new connection
            client_socket, client_address = server_socket.accept()

            # recieve the name of the client
            user = recieve_message(client_socket)

            # handle exception
            if user == False:
                continue

            # append the new socket to the read sockets list
            read_sockets.append(client_socket)

            # save username and username header
            clients[client_socket] = user

            print(
                f"accepted new connection from {client_address} : {user['data'].decode()}")

        # if existing socket is sending message
        else:

            # recieve message
            message = recieve_message(notified_socket)

            # if false client is disconnected, client cleanup
            if message == False:

                print(
                    f"connection closed from {clients[notified_socket]['data'].decode()}")

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # now we know that the client is not disconnected
            # get the client user name
            user = clients[notified_socket]
            print(
                f"recieved message from {user['data'].decode()} \n message => {message['data'].decode()}")

            # iterate over connected clients and broadcast the message

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user['header'] + user['data'] + message['header'] + message['data'])

     # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]

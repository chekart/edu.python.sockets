import socket
import messages
from messages import echo

def client_send_message(client_socket, message):
    """
    Send a message and try to get a receive
    """
    messages.send_message(client_socket, message)
    message = messages.read_message(client_socket)
    echo("[Client] Received: %s", message)
    

def client1(address):

    # creating socket ...
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ... and connecting to the server
    client_socket.connect(address)

    # send hello message and receive echo
    client_send_message(client_socket, "Hello")

    # shutting down sending
    client_socket.shutdown(socket.SHUT_WR)
    # getting bye message from the server
    echo("[Client] Received: %s", messages.read_message(client_socket))
    
    # waiting for the server to shut down
    if messages.read_message(client_socket) is None:
        echo("[Client] Got EOF from Server")

    client_socket.close()


def client2(address):

    # creating socket ...
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ... and connecting to the server
    client_socket.connect(address)

    # send hello message and receive echo
    client_send_message(client_socket, "Hello")

    # send bye message
    client_send_message(client_socket, "Bye")
    # the server should sent EOF
    if messages.read_message(client_socket) is None:
        echo("[Client] Got EOF from server")

        # shutting down read
        client_socket.shutdown(socket.SHUT_RD)
        # sending bye message to the server
        messages.send_message(client_socket, "Bye bye Server")
        messages.send_message(client_socket, "Have a good day")
        client_socket.shutdown(socket.SHUT_WR)

    client_socket.close()
"""
Simple messages format

Since TCP/IP is a stream, somehow we need to know bound of messages.
There are couple of strategies to do that:
    1. Use messages of fixed length
        example: 1024 bytes for each message, but in that case we have 1019 redundant bytes in "hello" message
    2. Use delimiter for messages
        example: with delimiter is ; message will look like this "hello;"
                 but in that case we need to escape delimiter to include it in message
    3. Use message length at the head of the message
        example: the hello message will look like this "\x05hello"
"""


def echo(message = "", *args):
    """
    Thread save newline
    """
    message = message % args + '\n'
    print message,


def read_message(connection_socket):
    """
    Read a message from specified socket
    """

    # first read length (for clarity we accept only messages up to 255)
    chunk = connection_socket.recv(1)
    # recv returns 0 bytes read if connection is shutdown
    if not chunk:
        return None
    length = ord(chunk)

    # start reading message. It's important to keep in mind the fact that TCP/IP it's a _stream_ protocol
    # and we don't have a guarantee that entire message will arrive at a single recv call
    message = ''
    while len(message) < length:
        chunk = connection_socket.recv(length - len(message))
        # actually an error since peer shut down sending before it sent entire message
        if not chunk:
            return None

        message += chunk

    return message

def send_message(connection_socket, message):
    """
        Send a message
    """
    connection_socket.send(chr(len(message)))

    # sending the message in a loop
    sent = 0
    while sent < len(message):
        chunk = connection_socket.send(message[sent:])
        # it's non blocking socket and it shouldn't return 0
        sent += chunk

    return True



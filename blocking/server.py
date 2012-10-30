import time
import socket
import threading
import messages

from messages import echo

class SimpleBlockingServer(object):
    """
    Wrapper around server functions
    """

    def __init__(self, address):
        self.__address = address
        
        self.__listen_thread = threading.Thread(target=SimpleBlockingServer.server_thread_target, args=[self])
        self.__started = False              # indicates that server is initialized and accepting client connections
        self.__accept_connections = True    # shall server accept new connections or should it leave listening loop
        self.__connections = []             # store server connection threads


    def __server_stop_listening(self):
        """
        Stop server from listening
        """
        self.__accept_connections = False

        try:
            # we're making dummy connection to force the server socket accept connection and return from blocking op
            closing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_socket.connect(self.__address)
            closing_socket.close()
        except:
            echo("[Server] Could connect to Server. Looks like server is down or not stared")
        

    def __server_wait_for_start(self):
        """
        Wait for server to initialize
        """
        while not self.__started:
            time.sleep(0)


    def __server_wait_for_end(self):
        """
        Wait for all server connections to finish their work
        """
        for connection in self.__connections:
            connection[0].join()


    @staticmethod
    def server_connection_thread_target(connection_socket, address):
        """
        Client-Server message loop. Just receiving messages and echoing back to the client.
        Special message "Bye" closes the connection
        WARNING: we assume that clients don't abuse the connection, i.e a client should end the connection, not the server
        """
        can_send = True

        try:

            while True:
                # reading one message from the client
                message = messages.read_message(connection_socket)
                if message is None:
                    # message is None, that means that the client has stopped sending data to the server
                    echo("[Server] Got EOF from Client")
                    # in that case we can shutdown reading
                    connection_socket.shutdown(socket.SHUT_RD)

                    # lets check if the server shut down sending first
                    if can_send:
                        # send bye message to the client ...
                        messages.send_message(connection_socket, "Bye bye Client")
                        # ... and shut down sending
                        connection_socket.shutdown(socket.SHUT_WR)

                    # nothing to send, nothing to receive, we can leave the message loop now
                    break

                echo("[Server] Received [%s]: %s", address, message)

                # lets check if the server can send messages
                if can_send:
                    # echoing message from the client
                    messages.send_message(connection_socket, message)

                    # if we received special message from the client
                    if message == "Bye":
                        # shut down sending to the client and start only to listen for the remaining client messages
                        connection_socket.shutdown(socket.SHUT_WR)
                        can_send = False

        except Exception:
            echo("[Server] Connection error")
        finally:
            echo("[Server] Closing socket")
            # close the socket
            connection_socket.close()


    @staticmethod
    def server_thread_target(server):
        """
        Accept thread
        """

        # creating a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            
            # binding socket to specified address
            server_socket.bind(server.__address)
            # start listening for connections
            server_socket.listen(2)

            # accept connection loop
            while server.__accept_connections:

                server.__started = True
                # wait for client connection
                connection_socket, connection_addr = server_socket.accept()
                # since closing listening socket not forces accept to throw exception we need to check a flag
                if server.__accept_connections:
                    # the server has connection with the client and we need to start a message loop
                    thread = threading.Thread(target = SimpleBlockingServer.server_connection_thread_target, args=[connection_socket, connection_addr])
                    server.__connections.append((thread, connection_socket))
                    thread.start()

                echo("[Server] Client %s connected", connection_addr)
                
        finally:
            # closing the server socket
            server_socket.close()
            echo("[Server] Closing server socket")


    def run(self):
        """
        Start the server in separate thread
        """
        self.__listen_thread.start()
        # wait for server to start
        self.__server_wait_for_start()

    def shutdown(self):
        """
        Stop the server
        """
        # wait for listening thread to end
        self.__server_stop_listening()
        # wait for all client connections to end
        self.__server_wait_for_end()
        self.__listen_thread.join()

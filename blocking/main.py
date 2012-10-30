"""
Created by: Chekanov A

*** Disclaimer
This program was created for education purposes only.
That means that the server will work in ideal environment.
Clients are ending the connection not the server. No timeouts and heartbeats supported

*** Algo
1. Start server which will be listening for client connections
2. Connect to the server
3. Send a hello message and receive same hello echo response
4. Shutdown write on the client socket (send EOF to the server)
5. Receive bye message from the server
6. Shutdown read on client socket and close the socket
7. Connect to the server
8. Send a hello message and receive same hello echo response
9. Send bye message to the server which will cause the server to shutdown sending to the client
10. Get EOF from the server and send to it bye message
11. Shut down write on the client socket and close the client socket
"""
from server import SimpleBlockingServer
import client

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)

# starting the server
server = SimpleBlockingServer(SERVER_ADDRESS)
server.run()

# starting first client
client.client1(SERVER_ADDRESS)
# starting second client
client.client2(SERVER_ADDRESS)

# shutting down the server
server.shutdown()
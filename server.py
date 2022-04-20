from re import X
import threading
import socket
import signal
import sys
import select

class chat_server:
    def signal_handler(self, signo, frame):
        for client in self.clients:
            # close clients socket descriptors
            client.close()
        print("Closing server.")
        sys.exit(0)

    def __init__(self):

        # make a socket, let reuse of the address
        self.serverDesc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverDesc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # listen for up to 5 clients
        self.MAX_CONN = 5
        self.clients = []
        self.usernames= []

        self.port = 5000
        self.host = "0.0.0.0"


        # bind ctrl c to the signal handler function
        signal.signal(signal.SIGINT, self.signal_handler)

        # bind the server to and address and listen
        self.serverDesc.bind((self.host,self.port))
        self.serverDesc.listen(self.MAX_CONN)

    def start(self):
        self.readSet = [self.serverDesc]

        while(True):
            # set up select to read from readSet
            readFromSet = self.readSet.copy()
            try:
                select.select(readFromSet, [], [])
            except Exception as e:
                print(e)
            
            for socketDesc in readFromSet:
                # server is ready to accept a connection
                if socketDesc == self.serverDesc:
                    clientDesc, address = self.serverDesc.accept()
                    print(clientDesc.fileno())

                    # at login the client passes its username to server, read it
                    clientUsername = clientDesc.recv(1024).decode()
                    print(clientUsername)

                    self.usernames.append(clientUsername)

                    # add clients socket descriptor to client list
                    self.clients.append(clientDesc)
                else:
                    # get the string passed from the client
                    data = socketDesc.recv(1024).decode()

                    if("chat @" in data):
                        print("message a specific user")
                    elif("chat" in data):
                        print("broadcast this msg to everyone")
                    elif("voice" in data):
                        # we are using voip
                        print("call voip function")
                    elif not data:
                        print("Empty string passed.")
                    else:
                        print("Bad data received")

    def send(self, incomingConnection):
        try:
            while(True):
                # chunk size if 4bytes, read that many in for voice
                data = incomingConnection.recv(4096)
                # 
                for client in self.clients:
                    if client != incomingConnection:
                        client.send(data)
        except:
            print("Client disconnected")
            # remove socket for user

server = chat_server()
server.start()

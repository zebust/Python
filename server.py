import socket
import select
import argparse

class ChatServer(object):

    def __init__(self, port):

        ServerPort=port
        self.ServerName = socket.gethostname()
        ServerAddress = socket.gethostbyname(socket.gethostname())
        bind_adress = (ServerAddress, ServerPort)


        self.outputs = []
        self.connections = 0

        self.S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.S_socket.bind(bind_adress)
        self.S_socket.listen(2)

        print("Server: %s is listning on IP: %s , PORT: %d" % (self.ServerName, ServerAddress, ServerPort))

    def run(self):
        inputs = [self.S_socket]
        while True:
            try:
                readable, writeable, exception = select.select(inputs, self.outputs, [],0.1)
                for sock in readable:
                    if sock == self.S_socket:  # server socket is updated with new connection request
                        ClientSocket, C_address = self.S_socket.accept()
                        print('New Connection recieved from ' + C_address[0] + ' : ' + str(C_address[1]))
                        send_msg = "Your are now connected to server:" + self.ServerName
                        ClientSocket.send(send_msg.encode('utf-8'))
                        inputs.append(ClientSocket)
                        self.outputs.append(ClientSocket)
                        self.connections += 1

                    else:
                        ClientMessage = sock.recv(1024).decode('utf-8')
                        if ClientMessage:
                            if ClientMessage == 'x':
                                print("Lost connection with Client")
                                inputs.remove(sock)
                                self.outputs.remove(sock)
                                self.connections -= 1
                                break
                            else:
                                self.sendMessage(sock,ClientMessage ) # client socket is updated with new data

            except KeyboardInterrupt:
                print("\nClosing Server...\n\n")
                self.S_socket.close()
                return


    def sendMessage(self, tunnel, message):
        for outgoingSocket in self.outputs:
            if outgoingSocket != tunnel:
                outgoingSocket.send( message.encode('utf-8'))


if __name__ == "__main__":

    # parser = argparse.ArgumentParser(description='Test Chat Server')
    # parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    # given_args = parser.parse_args()
    # port = given_args.port

    while True:
        port = 9997
        server = ChatServer(port)
        server.run()

        temp = input("Server closed....\n\nTo close window press 'x'. To start server again press 'Enter:'\n")
        if temp == "x":
            break
        else:
            pass
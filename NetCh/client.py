import socket
import select
import sys
import msvcrt

class ClientChat(object):

    def __init__(self, ServerPort, ServerAddress, name):

        connect_host = (ServerAddress, ServerPort)
        self.ClientName = name
        self.connected = False
        self.prompt = "Me:>> "

        self.ClienSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.ClienSocket.connect(connect_host)
            recv_msg = self.ClienSocket.recv(1024).decode('utf-8')
            print(recv_msg)
            self.connected = True
        except:
            print("Connection Failed")
            return


    def run(self):
            inputs = [self.ClienSocket]
            while self.connected:
                try:
                    readable, writeable, exceptional = select.select(inputs, [], [], 0.1)
                    for sock in readable:
                        if sock == self.ClienSocket:
                            ServerData = self.ClienSocket.recv(1024).decode('utf8')
                            print(ServerData)

                    if msvcrt.kbhit():
                        sys.stdout.write(self.prompt)
                        sys.stdout.flush()
                        ClientData = sys.stdin.readline().strip()
                        FinalMessage = self.ClientName + "@" + socket.gethostname() + ":>> " + ClientData
                        self.ClienSocket.send(FinalMessage.encode('utf8'))

                except KeyboardInterrupt:
                    print("\n\nClosing connection to server...\n")
                    self.ClienSocket.send("x".encode('utf-8'))
                    self.ClienSocket.close()
                    return

                except:
                    print("\n\nXXXXXXXXXXXXXXXXXXXXXXX...\n")
                    return

if __name__ == "__main__":

    print("\nTo end chat session press Ctrl+C at any time\n\n")

    while True:
        name = input("Enter Username: ")
        ServerAddress = input("Enter Server IP address: ")
        ServerPort =input("Server Port: ")


        Client = ClientChat(int(ServerPort), ServerAddress, name)
        Client.run()
        temp=input("Connection closed....\n\nTo close window press 'x'. To connect again press 'Enter:'\n")
        if temp == "x":
            break
        else:
            pass


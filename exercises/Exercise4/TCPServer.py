from socket import *
serverSocket = socket(AF_INET, SOCK_STREAM)

serverPort = 40000

serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while True:
    print "Waiting for message\n"
    connectionSocket, addr = serverSocket.accept()

    while True:
        message = connectionSocket.recv(1024)
        message = message.upper()
        connectionSocket.send(message)
        print "Message sent!\n"

connectionSocket.close()

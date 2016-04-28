                                
from socket import *
import time

serverName = '129.241.187.148'

serverPort = 40000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:

    sentence = raw_input('Input lowercase sentence: ')

    clientSocket.send(sentence)
    #clientSocket.send("+potet")                                                
    modifiedSentence = clientSocket.recv(1024)

    print "From server: ", modifiedSentence

clientSocket.close()

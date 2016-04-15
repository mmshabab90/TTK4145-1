# coding: utf-8

import SocketServer
import socket
import json
import time
from constants import *
from threading import Thread
from queue import Master

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    SocketServer.TCPServer.allow_reuse_address = True
    daemon_threads = True

class ClientHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.server.master.add_elevator(self.ip, MODEL, self.server.lock)

    def handle(self):
        while True:
            received_string = self.connection.recv(4096)
            received = json.loads(received_string)
            print "\nReceived:", received
            received = received.upper()
            print "Sent:", received

            self.request.sendall(received)

class Client():
    def __init__(self, host, server_port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        self.run()

    def run(self):
        self.connection.connect((self.host, self.server_port))


    def receive_msg(self, msg):
        print "Received:", msg

    def disconnect(self):
        self.connection.close()

    def send_msg(self, data):
        self.connection.sendall(json.dumps(data))

class Msg_receiver(Thread):
    def __init__(self, client, connection):
        super(Msg_receiver, self).__init__()
        self.daemon = True
        self.client = client
        self.connection = connection

    def run(self):
        while (True):
            data = self.connection.recv(4096)
            if (data):
                self.client.receive_msg(data)

# coding: utf-8

import SocketServer
import socket
import json
import time

from threading import Thread

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

class ClientHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

    def handle(self):
        while True:
            received_string = self.connection.recv(4096)
            received = json.loads(received_string)
            print "\nReceived:", received
            received = received.upper()
            print "Sent:", received

            self.request.sendall(received)


def master_broadcast():
    UDP_PORT = 39500
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while (True):
        sock.sendto('master', ('255.255.255.255', UDP_PORT))
        time.sleep(1)


class Client:
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

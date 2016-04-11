import SocketServer
import socket
import json
import time

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

def master_broadcast():
    UDP_PORT = 39500
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while (True):
        sock.sendto('master', ('255.255.255.255', UDP_PORT))
        time.sleep(1)

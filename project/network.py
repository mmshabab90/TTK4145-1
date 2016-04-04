import SocketServer
import json


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

class ClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.logged_in = False

        while True:
            received_string = self.connection.recv(4096)
            received = json.loads(received_string)

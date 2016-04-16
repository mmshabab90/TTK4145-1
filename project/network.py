# coding: utf-8

import SocketServer
import socket
import json
import time
from constants import *
from threading import Thread
from master import Master

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

class ClientHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.server.master.add_elevator(self.ip, ELEV_MODE)
        self.parser = Msg_parser(self.server.master)

    def handle(self):
        while True:
            received_string = self.connection.recv(4096)
            print received_string
            if (received_string):
                self.parser.parse(received_string)
                #Check message type:
                #'External'     - (floor number) find best elevator call assign_task(floor)
                #'Queue update' - (task_stack) set oldTS = NewTS at right ip
                #'Floor update' - (cur floor number) set current floor variable

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

    def send_msg(self, msg_type, data, ip):
        msg = {'type':msg_type, 'data':data, 'ip':ip}
        self.connection.sendall(json.dumps(msg))

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

class Msg_parser():
    def __init__(self, master):
        self.master = master
        self.possible_types = {
            'external': self.parse_external,
            'queue_update': self.parse_queue_update,
            'floor_update': self.parse_floor_update,
        }

    def parse(self, data):
        data = json.loads(data)
        print data
        if data['type'] in self.possible_types:
            self.possible_types[data['type']](data)
        else:
            return

    def parse_external(self, data):
        ip = self.master.assign_task(data['data'])
        print "Ip:", ip
        print "Data:", data['data']
        if (ip):
            self.master.elevators[ip].insert_task(data['data'])

    def parse_queue_update(self, data):
        self.master.elevators[data['ip']].task_stack = data['data']

    def parse_floor_update(self, data):
        self.master.elevators[data['ip']].current_floor = data['data']


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

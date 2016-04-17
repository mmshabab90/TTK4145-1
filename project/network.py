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
        self.server.clients[self.ip] = self
        self.server.master.add_elevator(self.ip, ELEV_MODE)
        self.parser = Msg_parser(self.server.master, self)

    def handle(self):
        connected = True
        while connected:
            received_string = self.connection.recv(4096)
            if (received_string):
                self.parser.parse(received_string)
            else:
                connected = False

    def finish(self):
        remaining_queue = self.server.master.elevators[self.ip].task_stack
        del self.server.master.elevators[self.ip]
        del self.server.clients[self.ip]
        for task in remaining_queue:
            ip = self.server.master.best_elev(task)
            if (ip and self.server.master.external_buttons[task]):
                self.server.master.elevators[ip].insert_task(task)
        for elev in self.server.master.elevators:
            self.server.clients[elev].send_msg('queue_update',
                                               self.server.master.elevators[elev].task_stack)

    def send_msg(self, msg_type, data):
        msg = {'type':msg_type, 'data':data}
        with self.server.master.lock:
            self.connection.sendall(json.dumps(msg))


class Client():
    def __init__(self, host, server_port, elev):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        self.elev = elev
        self.run()

    def run(self):
        self.connection.connect((self.host, self.server_port))

    def handle_msg(self, msg):
        received = json.loads(msg)
        if (received['type'] == 'queue_update'):
            self.elev.task_stack = received['data']

    def disconnect(self):
        self.connection.close()

    def send_msg(self, msg_type, data, ip):
        msg = {'type':msg_type, 'data':data, 'ip':ip}
        with self.elev.lock:
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
                self.client.handle_msg(data)

class Msg_parser():
    def __init__(self, master, client_handler):
        self.master = master
        self.client_handler = client_handler
        self.possible_types = {
            'external': self.parse_external,
            'queue_update': self.parse_queue_update,
            'floor_update': self.parse_floor_update,
        }

    def parse(self, data):
        data = json.loads(data)
        if data['type'] in self.possible_types:
            self.possible_types[data['type']](data)
        else:
            return

    def parse_external(self, data):
        self.master.external_buttons[data['data']] = True
        ip = self.master.best_elev(data['data'])
        if (ip):
            self.master.elevators[ip].insert_task(data['data'])
            self.client_handler.server.clients[ip].send_msg('queue_update',
                                         self.master.elevators[ip].task_stack)
        #notify backup

    def parse_queue_update(self, data):
        if (len(self.master.elevators[data['ip']].task_stack) > len(data['data'])):
            self.master.external_buttons[self.master.elevators[data['ip']].task_stack[0]] = False
            #notify backup
        self.master.elevators[data['ip']].task_stack = data['data']
        #Notify backup

    def parse_floor_update(self, data):
        self.master.elevators[data['ip']].current_floor = data['data']
        #notify backup


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

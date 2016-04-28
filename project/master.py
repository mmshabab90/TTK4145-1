"""Master module."""

import socket
import time
from threading import Thread, Lock
from os import system
import constants
import elev
import network

class Master(object):
    """Master object"""
    def __init__(self):
        self.alive = True
        self.elevators = {}
        self.ip = network.get_ip()
        self.backup_ip = ''
        self.external_buttons = [False for floor in range(constants.N_FLOORS)]
        self.lock = Lock()
        self.broadcaster = Thread(target=self.broadcast)
        self.broadcaster.setDaemon(True)
        self.broadcaster.start()
        self.server = network.ThreadedTCPServer((self.ip, 10001),
                                                network.ClientHandler)
        self.server.clients = {}
        self.server.master = self
        self.server_thread = Thread(target=self.run_server)
        self.server_thread.setDaemon(True)
        self.server_thread.start()

    def close(self):
        self.alive = False
        self.broadcaster.join()

    def add_elevator(self, ip, mode):
        self.elevators[ip] =  elev.Elev(mode)

    def best_elev(self, floor):
        if (not any(floor in elev.task_stack for elev in self.elevators.values())):
            if (all(elev.task_stack == [] for elev in self.elevators.values())):
                return self.closest_elev(floor)
            else:
                return self.fastest_elev(floor)

    def closest_elev(self, floor):
        min_dist = constants.N_FLOORS
        for elev in self.elevators:
            dist = abs(self.elevators[elev].current_floor - floor)
            if (dist < min_dist):
                min_dist = dist
                closest_elev = elev
        return closest_elev

    def fastest_elev(self, floor):
        shortest_time = 2*N_FLOORS*(constants.STOP_TIME + constants.TIME_BETWEEN_FLOORS)
        for elev in self.elevators:
            time = self.cal_time(elev, floor)
            if (time < shortest_time):
                shortest_time = time
                fastest_elev = elev
        return fastest_elev

    def cal_time(self, elev_ip, floor):
        elev = self.elevators[elev_ip]
        stops = len(elev.task_stack)

        if ((elev.next_dir() == constants.DIRN_UP and floor > elev.current_floor) or
            (elev.next_dir() == constants.DIRN_DOWN and floor < elev.current_floor)):
            distance = abs(elev.current_floor - floor)

        elif(elev.next_dir() == constants.DIRN_UP and floor <= elev.current_floor):
            distance = 2*max(elev.task_stack) - elev.current_floor - floor

        elif(elev.next_dir() == constants.DIRN_DOWN and floor >= elev.current_floor):
            distance = elev.current_floor + floor

        else:
            distance = abs(elev.current_floor - floor)

        return stops*constants.STOP_TIME + distance*constants.TIME_BETWEEN_FLOORS

    def broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while (self.alive):
            sock.sendto('master', ('255.255.255.255', 39500))
            time.sleep(1)

    def run_server(self):
        self.server.timeout = None
        while (True):
            self.server.handle_request()

    def print_system(self):
        while (True):
            system('clear')
            print "External buttons pressed:"
            print self.external_buttons
            print "Backup:", self.backup_ip[-3:]
            for elev in self.elevators.values():
                print "\n", self.elevators.keys()[self.elevators.values().index(elev)][-3:],
                print "----------[", elev.current_floor, "]"
                for task in elev.task_stack:
                    print task, " ",
                print "\n-------------------"
            time.sleep(0.5)

    def send_backup_ip(self):
        for elev in self.elevators:
            self.server.clients[elev].send_msg('backup_ip', self.backup_ip)

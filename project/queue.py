import socket
import time
from threading import Thread
from os import system
from constants import *
import elev

class Master():
    def __init__(self):
        self.alive = True
        self.elevators = {}
        self.broadcaster = Thread(target = self.broadcast)
        self.broadcaster.setDaemon(True)
        self.broadcaster.start()

    def __exit__(self):
        self.alive = False
        self.broadcaster.join()

    def add_elevator(self, ip, mode, lock):
        self.elevators[ip] =  elev.Elev(ip, mode, lock)

    def assign_task(self, floor):
        print self
        if (not any(floor in elev.task_stack for elev in self.elevators.values())):
            if (all(elev.task_stack == [] for elev in self.elevators.values())):
                elev = self.closest_elev(floor)
            else:
                elev = self.fastest_elev(floor)
        elevators[elev].insert_task(floor)

    def closest_elev(self, floor):
        min_dist = N_FLOORS
        for elev in self.elevators:
            dist = abs(elevators[elev].current_floor - floor)
            if (dist < min_dist):
                min_dist = dist
                closest_elev = elev
        return closest_elev

    def fastest_elev(self, floor):
        shortest_time = 2*N_FLOORS*(STOP_TIME + TIME_BETWEEN_FLOORS)
        for elev in self.elevators:
            time = self.cal_time(elev, floor)
            if (time < shortest_time):
                shortest_time = time
                fastest_elev = elev
        return fastest_elev

    def cal_time(self, elev_ip, floor):
        elev = self.elevators[elev_ip]
        stops = len(elev.task_stack)

        if ((elev.next_dir() == DIRN_UP and floor > elev.current_floor) or
            (elev.next_dir() == DIRN_DOWN and floor < elev.current_floor)):
            distance = abs(elev.current_floor - floor)

        elif(elev.next_dir() == DIRN_UP and floor <= elev.current_floor):
            distance = 2*max(elev.task_stack) - elev.current_floor - floor

        elif(elev.next_dir() == DIRN_DOWN and floor >= elev.current_floor):
            distance = elev.current_floor + floor

        else:
            distance = abs(elev.current_floor - floor)

        return stops*STOP_TIME + distance*TIME_BETWEEN_FLOORS

    def broadcast(self):
        UDP_PORT = 39500
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while (self.alive):
            sock.sendto('master', ('255.255.255.255', UDP_PORT))
            time.sleep(1)

    def print_task_stack(elev):
        system('clear')
        print "-------------------"
        for task in elev.task_stack:
            print task, " ",
        print "\n-------------------"

import elev
import socket
from os import system
from constants import *

class Elev(Master):
    def __init__(self, ipaddr):
        self.task_stack = []
        self.current_floor = 0
        self.ip = ipaddr

    def insert_task(self, floor):
        cur_dir = Master.elev_dir(self)
        if ((self.current_floor < floor and cur_dir == DIRN_UP) or
            (self.current_floor <= floor and cur_dir == DIRN_DOWN)):
            for task in self.task_stack:
                if (floor < task):
                    self.task_stack.insert(self.task_stack.index(task), floor)
                    return
        else:
            for task in self.task_stack:
                if (floor > task):
                    self.task_stack.insert(self.task_stack.index(task), floor)
                    return
        self.task_stack.append(floor)


class Master():
    def __init__(self):
        self.elevators = {}

    def add_elevator(self, ip):
        self.elevators[ip] = Elev(ip)

    def

    def assign_task(self, floor):
        elev = None
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

        if ((elev_dir(elev) == DIRN_UP and floor > elev.current_floor) or
            (elev_dir(elev) == DIRN_DOWN and floor < elev.current_floor)):
            distance = abs(elev.current_floor - floor)

        elif(elev_dir(elev) == DIRN_UP and floor <= elev.current_floor):
            distance = 2*max(elev.task_stack) - elev.current_floor - floor

        elif(elev_dir(elev) == DIRN_DOWN and floor >= elev.current_floor):
            distance = elev.current_floor + floor

        else:
            distance = abs(elev.current_floor - floor)

        return stops*STOP_TIME + distance*TIME_BETWEEN_FLOORS

    def elev_dir(elev):
        if (elev.task_stack != []):
            if(elev.current_floor < elev.task_stack[0]):
                return DIRN_UP
            else:
                return DIRN_DOWN
        else:
            return DIRN_STOP

# def print_task_stack():
#     #system('clear')
#     for stack in task_stacks:
#         print "-------------------"
#         for task in stack:
#             print task+1, " ",
#     print "\n-------------------"

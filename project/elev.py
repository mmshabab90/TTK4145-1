from ctypes import *
from constants import *
from threading import Thread, Lock
import network
import master
import time

class Elev(master.Master):
    def __init__(self, mode):
        self.alive = False
        self.lock = Lock()
        self.mode = mode
        self.task_stack = [0]
        self.current_floor = N_FLOORS
        self.master_addr = None
        self.state = 'client'

    def run(self):
        self.alive = True
        self.client = network.Client(self.master_addr, 10001, self)
        self.ip = network.get_ip()
        self.worker = network.Msg_receiver(self.client, self.client.connection)
        self.worker.setDaemon(True)
        self.worker.start()
        self.elev = cdll.LoadLibrary("../driver/driver.so")
        self.elev.elev_init(self.mode)
        self.movement = Thread(target = self.movement_handler)
        self.buttons = Thread(target = self.button_handler)
        self.movement.setDaemon(True)
        self.buttons.setDaemon(True)
        self.movement.start()
        self.buttons.start()

    def __exit__(self):
        if (self.alive):
            self.alive = False
            self.movement.join()
            self.buttons.join()
            self.worker.join()

    def insert_task(self, floor):
        next_dir = self.next_dir()
        if (next_dir == DIRN_STOP):
            self.task_stack.append(floor)
        elif ((self.current_floor < floor and next_dir == DIRN_UP) or
            (self.current_floor <= floor and next_dir == DIRN_DOWN)):
            for task in self.task_stack:
                if (floor < task):
                    self.lock.acquire(True)
                    self.task_stack.insert(self.task_stack.index(task), floor)
                    self.lock.release()
                    return
            self.task_stack.append(floor)
        else:
            for task in self.task_stack:
                if (floor > task):
                    self.lock.acquire(True)
                    self.task_stack.insert(self.task_stack.index(task), floor)
                    self.lock.release()
                    return
            self.task_stack.append(floor)

    def next_dir(self):
        if (self.task_stack != []):
            if(self.current_floor < self.task_stack[0]):
                return DIRN_UP
            else:
                return DIRN_DOWN
        else:
            return DIRN_STOP

    def movement_handler(self):
        print "start move handler"
        while (self.alive):
            if (self.task_stack != []):
                direction_set = 0
                while (self.current_floor != self.task_stack[0]):
                    if (self.task_stack[0] > self.current_floor and not direction_set):
                        self.elev.elev_set_motor_direction(DIRN_UP)
                        direction_set = 1
                    elif(self.task_stack[0] < self.current_floor and not direction_set):
                        self.elev.elev_set_motor_direction(DIRN_DOWN)
                        direction_set = 1
                    floor_sensor = self.elev.elev_get_floor_sensor_signal()
                    if (floor_sensor != -1 and floor_sensor != self.current_floor):
                        self.current_floor = floor_sensor
                        self.elev.elev_set_floor_indicator(floor_sensor)
                        self.client.send_msg('floor_update',
                                             self.current_floor,
                                             self.ip)
                self.elev.elev_set_motor_direction(DIRN_STOP)
                direction_set = 0
                self.elev.elev_set_button_lamp(BUTTON_COMMAND, self.task_stack[0], 0)
                self.elev.elev_set_door_open_lamp(1)
                time.sleep(3)
                self.elev.elev_set_door_open_lamp(0)
                self.task_stack.pop(0)
                self.client.send_msg('queue_update',
                                     self.task_stack,
                                     self.ip)

    def button_handler(self):
        print "Start button handler"
        prev = [[0 for i in range(N_BUTTONS)] for j in range(N_FLOORS)]
        while (self.alive):
            for floor in range(N_FLOORS):
                for button in range(N_BUTTONS):
                    v = self.elev.elev_get_button_signal(button, floor)
                    if (v and v != prev[floor][button]):
                        if (button == BUTTON_COMMAND):
                            if (floor not in self.task_stack):
                                self.insert_task(floor)
                                self.client.send_msg('queue_update',
                                                     self.task_stack,
                                                     self.ip)
                        else:
                            self.client.send_msg('external', floor, self.ip)
                    prev[floor][button] = v

from ctypes import *
from constants import *
from threading import Thread
import queue
import time

class Elev(queue.Master):
    def __init__(self, mode, lock):
        self.alive = True
        self.lock = lock
        self.task_stack = [0]
        self.current_floor = N_FLOORS
        self.elev = cdll.LoadLibrary("../driver/driver.so")
        self.elev.elev_init(mode)
        self.movement = Thread(target = self.movement_handler)
        self.buttons = Thread(target = self.button_handler)
        self.movement.setDaemon(True)
        self.buttons.setDaemon(True)
        self.movement.start()
        self.buttons.start()

    def __exit__(self):
        self.alive = False
        self.movement.join()
        self.buttons.join()

    def insert_task(self, floor):
        next_dir = self.next_dir()
        if (floor not in self.task_stack):
            if (next_dir == DIRN_STOP):
                self.lock.acquire(True)
                self.task_stack.append(floor)
                self.lock.release()
                queue.Master.print_task_stack(self)
            elif ((self.current_floor < floor and next_dir == DIRN_UP) or
                (self.current_floor <= floor and next_dir == DIRN_DOWN)):
                for task in self.task_stack:
                    if (floor < task):
                        self.lock.acquire(True)
                        self.task_stack.insert(self.task_stack.index(task), floor)
                        self.lock.release()
                        queue.Master.print_task_stack(self)
                        return
                self.task_stack.append(floor)
                queue.Master.print_task_stack(self)
            else:
                for task in self.task_stack:
                    if (floor > task):
                        self.lock.acquire(True)
                        self.task_stack.insert(self.task_stack.index(task), floor)
                        self.lock.release()
                        queue.Master.print_task_stack(self)
                        return
                self.task_stack.append(floor)
                queue.Master.print_task_stack(self)
            queue.Master.print_task_stack(self)

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
                direction_set = 0               #NEW

                while (self.current_floor != self.task_stack[0]):
                    if (self.task_stack[0] > self.current_floor and not direction_set): 
                        self.elev.elev_set_motor_direction(DIRN_UP)
                        direction_set = 1       #NEW
                    elif(self.task_stack[0] < self.current_floor and not direction_set):
                        self.elev.elev_set_motor_direction(DIRN_DOWN)
                        direction_set = 1       #NEW
                    floor_sensor = self.elev.elev_get_floor_sensor_signal()
                    if (floor_sensor != -1 and floor_sensor != self.current_floor):
                        self.current_floor = floor_sensor
                        self.elev.elev_set_floor_indicator(floor_sensor)
                self.elev.elev_set_motor_direction(DIRN_STOP)
                direction_set = 0               #NEW
                self.elev.elev_set_button_lamp(BUTTON_COMMAND, self.task_stack[0], 0)
                self.elev.elev_set_door_open_lamp(1)
                time.sleep(3)
                self.elev.elev_set_door_open_lamp(0)
                self.lock.acquire(True)
                self.task_stack.pop(0)
                self.lock.release()
                queue.Master.print_task_stack(self)

    def button_handler(self):
        #Incapable of multiple simultaneous button presses.
        #Consider moving to a list based system
        #button_pressed = False
        print "Start button handler"
        prev = [[0 for i in range(N_BUTTONS)] for j in range(N_FLOORS)]
        while (self.alive):
            for floor in range(N_FLOORS):
                for button in range(N_BUTTONS):
                    v = self.elev.elev_get_button_signal(button, floor)
                    if (v and v != prev[floor][button]):
                        self.insert_task(floor)
                    prev[floor][button] = v

            # request = (-1,-1)
            # for button_type in range(N_BUTTONS):
            #     for floor in range(N_FLOORS):
            #         if (self.elev.elev_get_button_signal(button_type, floor)):
            #             request = (button_type, floor)
            # if (request != (-1,-1) and not button_pressed):
            #     button_pressed = True
            #     #TODO: Send external buttons to master
            #     self.lock.acquire(True)
            #     self.insert_task(request[1])
            #     self.lock.release()
            #     queue.Master.print_task_stack(self)
            # if (request == (-1,-1) and button_pressed):
            #     button_pressed = False
            


        #FORSLAG
        #print "Start button handler"
        #prev = [[0 for i in range(N_BUTTONS)] for j in range(N_FLOORS)]
        #while (self.alive):
        #    for floor in range(N_FLOORS):
        #        cmnd = self.elev.elev_get_button_signal(BUTTON_COMMAND, floor)
        #        if (cmnd and cmnd != prev[floor][BUTTON_COMMAND]):
        #            self.insert_task(floor)
        #        prev[floor][BUTTON_COMMAND] = cmnd
        #        for button in range(N_BUTTONS-1):
        #            req = self.elev.elev_get_button_signal(button, floor)
        #            if (req and req != prev[floor][button]):
        #                #Speak with master
        #            prev[floor][button] = v
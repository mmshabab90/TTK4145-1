from ctypes import *
from constants import *
import time
import queue

elev = cdll.LoadLibrary("../driver/driver.so")

elev.elev_init(0)

def check_buttons():
    for button_type in range(N_BUTTONS):
        for floor in range(N_FLOORS):
            if (elev.elev_get_button_signal(button_type, floor)):
                return (button_type, floor)
    return (-1,-1)

def go_to_floor(lock):
    #print "Go_to_floor called"
    while (True):
        if (queue.task_stacks[0] != []):
     #       print "Stack is not empty"
            while (queue.elev_cur_floor[0] != queue.task_stacks[0][0]):
                if (queue.task_stacks[0][0] > queue.elev_cur_floor[0]):
                    elev.elev_set_motor_direction(DIRN_UP)
                else:
                    elev.elev_set_motor_direction(DIRN_DOWN)
                floor_sensor = elev.elev_get_floor_sensor_signal()
                if (floor_sensor != -1 and floor_sensor != queue.elev_cur_floor[0]):
                    print "Floor:", floor_sensor
                    #queue.print_task_stack()
                    queue.elev_cur_floor[0] = floor_sensor
                    elev.elev_set_floor_indicator(floor_sensor)
            elev.elev_set_motor_direction(DIRN_STOP)
            elev.elev_set_button_lamp(BUTTON_COMMAND, queue.task_stacks[0][0], 0)
            lock.acquire(True)
            queue.task_stacks[0].pop(0)
            lock.release()
            queue.print_task_stack()
            elev.elev_set_door_open_lamp(1)
            time.sleep(3)
            elev.elev_set_door_open_lamp(0)

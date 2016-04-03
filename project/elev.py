from ctypes import *
from constants import *

elev = cdll.LoadLibrary("../driver/driver.so")

elev.elev_init(1)

def go_to_floor(desired_floor, init_floor):
    current_floor = init_floor
    elev.elev_set_door_open_lamp(0)
    while (current_floor != desired_floor):
        if(desired_floor>current_floor):
            elev.elev_set_motor_direction(DIRN_UP)
        else:
            elev.elev_set_motor_direction(DIRN_DOWN)
        if (elev.elev_get_floor_sensor_signal() != -1):
            current_floor = elev.elev_get_floor_sensor_signal()
            elev.elev_set_floor_indicator(current_floor)
    elev.elev_set_motor_direction(DIRN_STOP)
    elev.elev_set_button_lamp(BUTTON_COMMAND, desired_floor, 0)
    elev.elev_set_door_open_lamp(1)

def check_buttons():
    for button_type in range(N_BUTTONS):
        for floor in range(N_FLOORS):
            if (elev.elev_get_button_signal(button_type, floor)):
                return (button_type, floor)
    return (-1,-1)

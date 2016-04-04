import elev
from os import system
from constants import *

task_stacks = []
elev_cur_floor = []

def init(n_elev):
    for i in range(n_elev):
        task_stacks.append([])
        elev_cur_floor.append(0)

def assign_task(button_type, floor):
    
    
    # idle_elev = closest_idle_elev(floor)
    # if (idle_elev != -1 and not any(floor in stack for stack in task_stacks)):
    #     task_stacks[idle_elev].append(floor)
    # else:
    #     pass
    # print_task_stack()

def closest_elev(floor):
    min_dist = N_FLOORS
    closest_elev = -1
    for stack in task_stacks:
        elev = task_stacks.index(stack)
        dist = abs(elev_cur_floor[elev]-floor)
        if (dist < min_dist):
            min_dist = dist
            closest_elev = elev
    return closest_elev

def print_task_stack():
    system('clear')
    for stack in task_stacks:
        print "-------------------"
        for task in stack:
            print task, " "
    print "-------------------"

def cal_time(elev, floor):
    time = len(task_stacks(elev))*STOP_TIME + abs(elev_cur_floor(elev) - floor)
    return time

def compare_time_elevators(floor):
    smallest_elev = -1
    smallest_time = N_FLOORS*(STOP_TIME + TIME_BETWEEN_FLOORS)
    for elev in task_stacks:
        time = cal_time(elev,floor)
        if(time<smallest_time):
            smallest_time = time
            smallest_elev = elev
    return smallest_elev


import elev
from os import system
from constants import *

task_stacks = []
elev_cur_floor = []

def init(n_elev):
    for i in range(n_elev):
        task_stacks.append([])
        elev_cur_floor.append(0)

def assign_task(floor):
    elev = None
    if(not any(floor in stack for stack in task_stacks)):
        if(all(tasks == [] for tasks in task_stacks)):
            elev = closest_elev(floor)
        else:
            elev = fastest_elev(floor)
        insert_task(elev, floor)

def insert_task(elev, floor):
    cur_floor = elev_cur_floor[elev]
    cur_dir = elev_dir(elev)
    if((cur_floor < floor and cur_dir == DIRN_UP) or
       (cur_floor <= floor and cur_dir == DIRN_DOWN)):
        for task in task_stacks[elev]:
            if (floor < task):
                task_stacks[elev].insert(task_stacks[elev].index(task), floor)
                return
    else:
        for task in task_stacks[elev]:
            if (floor > task):
                task_stacks[elev].insert(task_stacks[elev].index(task), floor)
                return
    task_stacks[elev].append(floor)



def closest_elev(floor):
    min_dist = N_FLOORS
    closest_elev = None
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
            print task+1, " ",
    print "\n-------------------"

def cal_time(stack, floor):
    elev = task_stacks.index(stack)
    stops = len(task_stacks[elev])
    distance = N_FLOORS*2

    if((elev_dir(elev) == DIRN_UP and floor > elev_cur_floor[elev]) or
       (elev_dir(elev) == DIRN_DOWN and floor < elev_cur_floor[elev])):
        distance = abs(elev_cur_floor[elev] - floor)
    elif(elev_dir(elev) == DIRN_UP and floor <= elev_cur_floor[elev]):
        distance = 2*max(task_stacks[elev]) - elev_cur_floor[elev] - floor
    elif(elev_dir(elev) == DIRN_DOWN and floor >= elev_cur_floor[elev]):
        distance = elev_cur_floor[elev] + floor
    else:
        distance = abs(elev_cur_floor[elev] - floor)

    time = stops*STOP_TIME + distance*TIME_BETWEEN_FLOORS
    return time

def fastest_elev(floor):
    fastest_elev = None
    smallest_time = 2*N_FLOORS*(STOP_TIME + TIME_BETWEEN_FLOORS)
    for elev in task_stacks:
        time = cal_time(elev,floor)
        if(time<smallest_time):
            smallest_time = time
            fastest_elev = task_stacks.index(elev)
    return fastest_elev

def elev_dir(elev):
    if (task_stacks[elev] != []):
        if(elev_cur_floor[elev] < task_stacks[elev][0]):
            return DIRN_UP
        elif(elev_cur_floor[elev] > task_stacks[elev][0]):
            return DIRN_DOWN

    return DIRN_STOP

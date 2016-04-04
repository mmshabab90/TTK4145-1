import elev
import queue
from constants import *

def main():
    queue.init(N_ELEV)
    while (True):
        request = elev.check_buttons()
        if (request != (-1,-1)):
            queue.assign_task(request[1])
            elev.go_to_floor(queue.task_stacks[0][0], queue.elev_cur_floor[0])

if __name__ == "__main__":
    main()

import elev
import queue
from constants import *

def main():
    queue.init(N_ELEV)
    while (True):
        request = elev.check_buttons()
        if (request != (-1,-1)):
            queue.assign_task(request[0], request[1])

if __name__ == "__main__":
    main()

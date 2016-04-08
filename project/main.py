import elev
import queue
import network

from threading import Thread, Lock
from constants import *

def check_and_assign(lock):
    button_pressed = False
    while (True):
        request = elev.check_buttons()
        if (request != (-1,-1) and not button_pressed):
            button_pressed = True
            lock.acquire(True)
            queue.assign_task(request[1])
            lock.release()
        if (request == (-1,-1) and button_pressed):
            button_pressed = False

def main():
    HOST, PORT = 'localhost', 9998
    server = network.ThreadedTCPServer((HOST,PORT), network.ClientHandler)
    server.serve_forever()

    queue.init(N_ELEV)
    lock = Lock()
    button_thread = Thread(target = check_and_assign, args = (lock,))
    task_thread = Thread(target = elev.go_to_floor, args = (lock,))
    button_thread.setDaemon(True)
    button_thread.start()

    task_thread.setDaemon(True)
    task_thread.start()

    button_thread.join()
    task_thread.join()



if __name__ == "__main__":
    main()

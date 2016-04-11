import elev
import queue
import network
import socket

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
            queue.print_task_stack()
        if (request == (-1,-1) and button_pressed):
            button_pressed = False

def main():
    #Check for master on network, if not : state = master, else:
    #Check for backup on network, if not : state = backup, else:
    #State = client
    UDP_PORT = 39500
    state = None
    HOST, PORT = None,None
    server = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 39500))
    sock.settimeout(3)
    broadcast_thread = Thread(target = network.master_broadcast, args = (),)
    try:
        msg, addr = sock.recv(4096)
        if (msg == 'master'):
            state = 'client'
    except (socket.timeout):
        state = 'master'
        broadcast_thread.setDaemon(True)
        broadcast_thread.start()



    if (state == 'master'):
        HOST, PORT = 'localhost', 9998
        server = network.ThreadedTCPServer((HOST,PORT), network.ClientHandler)
        queue.init(N_ELEV)
    lock = Lock()

    button_thread = Thread(target = check_and_assign, args = (lock,))
    task_thread = Thread(target = elev.go_to_floor, args = (lock,))
    button_thread.setDaemon(True)
    button_thread.start()

    task_thread.setDaemon(True)
    task_thread.start()

    server.serve_forever()

if __name__ == "__main__":
    main()


def main():
    UDP_PORT = 39500
    state = None
    HOST, PORT = None,None
    server = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 39500))
    sock.settimeout(3)
    broadcast_thread = Thread(target = network.master_broadcast, args = (),)
    try:
        msg, addr = sock.recv(4096)
        if (msg == 'master'):
            state = 'client'
    except (socket.timeout):
        state = 'master'

    lock = Lock()
    button_thread = Thread(target = check_and_assign, args = (lock,))
    task_thread = Thread(target = elev.go_to_floor, args = (lock,))
    button_thread.setDaemon(True)
    button_thread.start()
    task_thread.setDaemon(True)
    task_thread.start()


    if(state == 'master'):
        init_master()


def init_master():
    queue.init()
    HOST, PORT = 'localhost', 9998
    server = network.ThreadedTCPServer((HOST,PORT), network.ClientHandler)
    master_thread = Thread(target = master(), args = (),)
    master_thread.setDaemon(True)
    master_thread.start()
    master_thread.join()

def init_client():
    pass

def init_backup():
    pass

def master():
    while (state == 'master'):
        pass
    #handle change state

def client():
    pass

def backup():
    pass

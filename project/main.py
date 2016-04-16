from elev import Elev
from master import Master
import network
import socket

from threading import Thread, Lock
from constants import *



def main():
    m_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    m_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    m_sock.bind(('', 39500))
    m_sock.settimeout(3)
    try:
        msg, master_addr = m_sock.recvfrom(4096)
        #state = 'client'
        b_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        b_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        b_sock.bind(('',39501))
        b_sock.settimeout(3)
        try:
            msg, backup_addr = b_sock.recvfrom(4096)
            state = 'client'
        except (socket.timeout):
            state = 'backup'
        b_sock.close()

    except (socket.timeout):
        state = 'master'
    m_sock.close()

    if (state == 'master'):
        print "Initiating.."
        master = Master(state, 39500)
        master.run()
        print "Ready to serve"
        print_thread = Thread(target = master.print_system)
        print_thread.setDaemon(True)
        print_thread.start()
        elev = Elev(ELEV_MODE)
        elev.master_addr = master.ip
        elev.run()
        running = True
        while running:
            raw = raw_input()
            if raw == "exit":
                running = False

    elif (state == 'backup'):
        elev = Elev(ELEV_MODE)
        elev.master_addr = master_addr[0]
        elev.run()
        backup = Master(state, 39501)
        print "I'M A BACKUP"
        running = True
        while running:
            raw = raw_input()
            if raw == "exit":
                running = False
    else:
        elev = Elev(ELEV_MODE)
        elev.master_addr = master_addr[0]
        elev.run()
        running = True
        while running:
            raw = raw_input()
            if raw == "exit":
                running = False
                elev.client.disconnect()
            else:
                pass
if __name__ == "__main__":
    main()

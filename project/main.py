from elev import Elev
from master import Master
import network
import socket
import states

from threading import Thread, Lock
from constants import *

def main():
    m_sock = network.socket_setup(39500)
    try:
        msg, master_addr = m_sock.recvfrom(4096)

        b_sock = network.socket_setup(39501)
        try:
            msg, backup_addr = b_sock.recvfrom(4096)
            state = 'slave'
        except (socket.timeout):
            state = 'backup'
        b_sock.close()

    except (socket.timeout):
        state = 'master'
    if(state != 'backup'):
        m_sock.close()

    if (state == 'master'):
        print "Initiating.."
        master = Master()
        master.run()
        print "Ready to serve"
        print_thread = Thread(target = master.print_system)
        print_thread.setDaemon(True)
        print_thread.start()
        elev = Elev(ELEV_MODE)
        elev.state = 'master'
        elev.master_addr = master.ip
        elev.run()
        states.master()

    else:
        elev = Elev(ELEV_MODE)
        elev.master_addr = master_addr[0]
        elev.run()
        Running = True
        states.slave(elev)
        backup = Master()
        elev.backup = backup
        states.backup(elev, backup)
        states.master()

if __name__ == "__main__":
    main()

import socket
from threading import Thread, Lock

import elev
import master
import network
import states
import constants

def main():
    m_sock = network.socket_setup(39500)
    try:
        msg, master_addr = m_sock.recvfrom(4096)

    except (socket.timeout):
        state = 'master'
    m_sock.close()

    if (state == 'master'):
        master = master.Master()
        master.run()
        print_thread = Thread(target = master.print_system)
        print_thread.setDaemon(True)
        print_thread.start()
        elev = elev.Elev(constants.ELEV_MODE)
        elev.state = 'master'
        elev.master_addr = master.ip
        elev.run()
        states.master()

    else:
        elev = elev.Elev(constants.ELEV_MODE)
        elev.master_addr = master_addr[0]
        elev.run()
        Running = True
        states.slave(elev)
        backup = master.Master()
        elev.backup = backup
        states.backup(elev, backup)
        states.master()

if __name__ == "__main__":
    main()

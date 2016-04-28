"""Main module"""

from threading import Thread
import socket
import elev as elevator
import master
import network
import states
import constants

def main():
    """Run on program start.

    Checks for other masters and initiates itself as either master or slave.

    """
    m_sock = network.socket_setup(39500)
    try:
        master_addr = m_sock.recvfrom(4096)[1]
    except socket.timeout:
        state = 'master'
    m_sock.close()

    if state == 'master':
        mstr = master.Master()
        mstr.run()
        print_thread = Thread(target=mstr.print_system)
        print_thread.setDaemon(True)
        print_thread.start()
        elev = elevator.Elev()
        elev.state = 'master'
        elev.master_addr = mstr.ip
        elev.run(constants.ELEV_MODE)
        states.master()

    else:
        elev = elevator.Elev()
        elev.master_addr = master_addr[0]
        elev.run(constants.ELEV_MODE)
        states.slave(elev)
        backup = master.Master()
        elev.backup = backup
        states.backup(elev, backup)
        states.master()

if __name__ == "__main__":
    main()

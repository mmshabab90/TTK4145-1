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
        #state = 'client'
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
        master = Master(state, 39500)
        master.run()
        print "Ready to serve"
        print_thread = Thread(target = master.print_system)
        print_thread.setDaemon(True)
        print_thread.start()
        elev = Elev(ELEV_MODE)
        elev.master_addr = master.ip
        elev.run()
        states.master()


    elif (state == 'backup'):
        elev = Elev(ELEV_MODE)
        elev.master_addr = master_addr[0]
        elev.run()
        backup = Master(state, 39501)
        print "I'M A BACKUP"
        states.backup()
        backup.run()
        elev.client = Client(backup.ip, 10001, backup)
        elev.master_addr = backup.ip
        worker.alive = False
        worker.join()
        elev.worker = network.Msg_receiver(elev.client, elev.client.connection)
        elev.worker.setDaemon(True)
        elev.worker.start()
        states.master()

    #Run until it die, or master die
    #if (old_master dies):
    #   old_backup -> new_master
    #   new_master setup one new backup on one arbitrary elev
    #As new master need to notify one elev to become new backup

    else:
        elev = Elev(ELEV_MODE)
        elev.master_addr = master_addr[0]
        elev.run()
        running = True
        while running:
            try:
                pass
            except(KeyboardInterrupt):
                running = False
                elev.client.disconnect()

    #Run til it die, or master/backup die
    #if(elev die):
    #   do task_stack, become unavailable (door close after taskstack done)
    #if(master die):
    #   setup new client to new master/server
    #   listen for command setup backup(from master)
    #if(back_up die):
    #   listen for command setup backup(from master)

if __name__ == "__main__":
    main()

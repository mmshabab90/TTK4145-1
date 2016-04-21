import network
import socket

def master():
    while (True):
        try:
            pass
        except(KeyboardInterrupt):
            print "Ctrl+C: User ended process"

def backup(elev, backup):
        listen_master = network.socket_setup(39500)
        while elev.state == 'backup':
            backup.print_system()
            try:
                msg = listen_master.recv(4096)
            except(socket.timeout):
                state = 'master'
                listen_master.close()
                backup.backup_ip = ''
                backup.run()
                #Change state to master
                #Clear all backup attributes
            except(KeyboardInterrupt):
                backup = False
                listen_master.close()

def slave(elev):
        while (elev.state == 'slave'):
                try:
                        pass
                except(KeyboardInterrupt):
                        elev.alive = False

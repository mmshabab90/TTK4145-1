import network
import socket

def master(elev):
    while (elev.state == 'master'):

    	except(KeyboardInterrupt):
            running = False
            listen_backup.close()

def backup(elev):
        listen_master = network.socket_setup( 39500)
        backup = True
        while backup:
                try:
                        msg = listen_master.recv(4096)
                except(socket.timeout):
                #Change state to master
                #Clear all backup attributes
                        backup = False
                        listen_master.close()
                except(KeyboardInterrupt):
                        backup = False
                        listen_master.close()

def slave(elev):
	while (elev.state == 'slave'):
		try:
			pass
		except(KeyboardInterrupt):
			elev.alive = False
			


        

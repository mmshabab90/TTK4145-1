import network
import socket

def master():
	listen_backup = network.socket_setup(39501)
	running = True
	while running:
		try:
			msg, bckup_addr = listen_backup.recvfrom(4096)
		except(socket.timeout):
			#Assign one elev backup functionality, if possible
			print "missing backup"
		except(KeyboardInterrupt):
			running = False
			listen_backup.close()
	

def backup():
	listen_master = network.socket_setup( 39500)
	backup = True
	while backup:
		try:
			msg = listen_master.recv(4096)
		except(socket.timeout):
		#Change state to master
			backup = False
			master = True
			listen_master.close()
		except(KeyboardInterrupt):
			backup = False
			listen_master.close()
	while master:
		pass

def slave():
	pass

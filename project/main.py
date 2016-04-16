from elev import Elev
from master import Master
import network
import socket

from threading import Thread, Lock
from constants import *



def main():
    UDP_PORT = 39500
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 39500))
    sock.settimeout(3)
    try:
        msg, master_addr = sock.recvfrom(4096)
        if (msg == 'master'):
            state = 'client'
    except (socket.timeout):
        state = 'master'
    sock.close()

    if (state == 'master'):
        print "Initiating.."
        master = Master()
        print "Ready to serve"
        print_thread = Thread(target = master.print_system)
        print_thread.setDaemon(True)
        print_thread.start()
        master.server.serve_forever()
    else:
        # client = network.Client(master_addr[0], 10001)
        # worker = network.Msg_receiver(client, client.connection)
        # worker.setDaemon(True)
        # worker.start()
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

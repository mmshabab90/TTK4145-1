from elev import Elev
from queue import Master
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
        msg = sock.recv(4096)
        if (msg == 'master'):
            state = 'client'
    except (socket.timeout):
        state = 'master'

    if (state == 'master'):
        print "Initiating master"
        master = Master()
        print "Initiating server"
        server = network.ThreadedTCPServer(('localhost',10001), network.ClientHandler)
        server.master = master
        server.lock = Lock()
        server.serve_forever()
    else:
        client = network.Client('localhost', 10001)
        worker = network.Msg_receiver(client, client.connection)
        worker.setDaemon(True)
        worker.start()
        running = True
        while running:
            raw = raw_input()
            if raw == "exit":
                running = False
                client.disconnect()
            else:
                client.send_msg(raw)

if __name__ == "__main__":
    main()

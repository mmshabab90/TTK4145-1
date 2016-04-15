from elev import Elev
from queue import Master
import network
import socket

from threading import Thread, Lock
from constants import *

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

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
        my_ip = get_ip()
        master = Master()
        server = network.ThreadedTCPServer((my_ip,10001), network.ClientHandler)
        server.master = master
        server.lock = Lock()
        print "Ready to serve"
        server.serve_forever()
    else:
        client = network.Client(master_addr, 10001)
        worker = network.Msg_receiver(client, client.connection)
        worker.setDaemon(True)
        worker.start()
        lock = Lock()
        elev = Elev(ELEV_MODE, lock)
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

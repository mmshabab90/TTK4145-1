import elev
import queue
import network

from constants import *


def main():
    HOST, PORT = 'localhost', 9998
    server = network.ThreadedTCPServer((HOST,PORT), network.ClientHandler)
    server.serve_forever()

    queue.init(N_ELEV)
    while (True):
        request = elev.check_buttons()
        if (request != (-1,-1)):
            queue.assign_task(request[0], request[1])



if __name__ == "__main__":
    main()

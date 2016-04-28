from socket import *

class Peer:
    def __init__(self):
        self.next_node = raw_input('Next node: ')
        self.next_next_node = raw_input('Next-next node: ')
        

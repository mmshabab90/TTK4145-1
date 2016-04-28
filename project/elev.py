"""Elevator module"""

from ctypes import cdll
import constants
from threading import Thread, Lock
import network
import time

class Elev(object):

    """Handle buttons, movement and server communication.

    Initialize as a dummy object, doesn't actually do anything until run() is
    called.
    """

    def __init__(self, mode):
        self.alive = False
        self.lock = Lock()
        self.mode = mode
        self.task_stack = [0]
        self.current_floor = constants.N_FLOORS
        self.master_addr = None
        self.state = 'slave'

    def run(self):
        """Start communication with master, movement- and button handler.

        Elev objects are used as a mirror of the real clients on the master
        side, so to initiate connection with the server, move the elevator,
        etc this must be called.
        """
        self.alive = True
        self.client = network.Client(self.master_addr, 10001, self)
        self.ip = network.get_ip()
        self.backup_ip = ''
        self.backup = None
        self.client.send_msg('request_backup_ip', None, self.ip)
        self.worker = network.Msg_receiver(self.client, self.client.connection)
        self.worker.setDaemon(True)
        self.worker.start()
        self.elev = cdll.LoadLibrary("../driver/driver.so")
        self.elev.elev_init(self.mode)
        self.movement = Thread(target=self.movement_handler)
        self.buttons = Thread(target=self.button_handler)
        self.movement.setDaemon(True)
        self.buttons.setDaemon(True)
        self.movement.start()
        self.buttons.start()

    def close(self):
        """Cleanup function.

        Should always be called explicitly when an elevator object goes out of
        scope.
        """
        if self.alive:
            self.alive = False
            self.movement.join()
            self.buttons.join()
            self.worker.join()

    def insert_task(self, floor):
        """Insert a given floor at the correct place in the queue.

        Considers the current state and direction of the elevator and places the
        new floor at the "best" position in the queue.

        Args:
        floor: The floor to be inserted
        """
        next_dir = self.next_dir()
        if next_dir == constants.DIRN_STOP:
            self.task_stack.append(floor)
        elif ((self.current_floor < floor and next_dir == constants.DIRN_UP) or
              (self.current_floor <= floor and next_dir == constants.DIRN_DOWN)):
            for task in self.task_stack:
                if floor < task:
                    self.lock.acquire(True)
                    self.task_stack.insert(self.task_stack.index(task), floor)
                    self.lock.release()
                    return
            self.task_stack.append(floor)
        else:
            for task in self.task_stack:
                if floor > task:
                    self.lock.acquire(True)
                    self.task_stack.insert(self.task_stack.index(task), floor)
                    self.lock.release()
                    return
            self.task_stack.append(floor)

    def next_dir(self):
        """Calculates the next direction of the elevator.

        Returns:
        Either DIRN_UP, DIRN_DOWN or DIRN_STOP. All defined in constants.py.
        """
        if self.task_stack != []:
            if self.current_floor < self.task_stack[0]:
                return constants.DIRN_UP
            else:
                return constants.DIRN_DOWN
        else:
            return constants.DIRN_STOP

    def movement_handler(self):
        """Monitor the queue and handle movement to the next task.

        Runs in its own thread, continuously monitoring the queue and moves the
        elevator in the direction of the next task.
        """
        while self.alive:
            if self.task_stack != []:
                direction_set = 0
                while self.current_floor != self.task_stack[0]:
                    if self.task_stack[0] > self.current_floor and not direction_set:
                        self.elev.elev_set_motor_direction(constants.DIRN_UP)
                        direction_set = 1
                    elif self.task_stack[0] < self.current_floor and not direction_set:
                        self.elev.elev_set_motor_direction(constants.DIRN_DOWN)
                        direction_set = 1
                    floor_sensor = self.elev.elev_get_floor_sensor_signal()
                    if floor_sensor != -1 and floor_sensor != self.current_floor:
                        self.current_floor = floor_sensor
                        self.elev.elev_set_floor_indicator(floor_sensor)
                        self.client.send_msg('floor_update',
                                             self.current_floor,
                                             self.ip)
                self.elev.elev_set_motor_direction(constants.DIRN_STOP)
                direction_set = 0
                self.elev.elev_set_button_lamp(constants.BUTTON_COMMAND,
                                               self.task_stack[0],
                                               0)
                self.elev.elev_set_door_open_lamp(1)
                time.sleep(3)
                self.elev.elev_set_door_open_lamp(0)
                self.task_stack.pop(0)
                self.client.send_msg('queue_update',
                                     self.task_stack,
                                     self.ip)

    def button_handler(self):
        """Monitor buttons and handle the pressing of said buttons.

        Runs in its own thread, continuously checks the systems buttons, and if
        a button is pressed it handles it accordingly.
        """
        prev = [[0 for i in range(constants.N_BUTTONS)]
                for j in range(constants.N_FLOORS)]
        while self.alive:
            for floor in range(constants.N_FLOORS):
                for button in range(constants.N_BUTTONS):
                    button_state = self.elev.elev_get_button_signal(button, floor)
                    if button_state and button_state != prev[floor][button]:
                        if button == constants.BUTTON_COMMAND:
                            if floor not in self.task_stack:
                                self.insert_task(floor)
                                self.client.send_msg('queue_update',
                                                     self.task_stack,
                                                     self.ip)
                        else:
                            self.client.send_msg('external', floor, self.ip)
                    prev[floor][button] = button_state

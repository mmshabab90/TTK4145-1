import socket
import time
import subprocess



is_backup = False

UDP_IP = '127.0.0.1'
UDP_PORT = 40001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((UDP_IP, UDP_PORT))

sock.settimeout(3)

try:
    sock.recvfrom(1024)
    is_backup = True
    last_recv = time.time()
except (socket.timeout):
    subprocess.call(['gnome-terminal', '-e', 'python /home/student/GR76/TTK4145/Exercise6/phoenix.py'])

count = 0

while True:
    if is_backup:
       while True:
           try:
               data, addr = sock.recvfrom(1024)
               count = int(data)
           except (socket.timeout):
               is_backup = False
               subprocess.call(['gnome-terminal', '-e', 'python /home/student/GR76/TTK4145/Exercise6/phoenix.py'])

               break
    else:
        while True:
            message = str(count)
            sock.sendto(message, (UDP_IP, UDP_PORT))
            print count
            count += 1
            time.sleep(1)

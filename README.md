#Project in TTK4145
##Implementation
### Driver
The driver is implemented using ctypes. A simple example is shown in
example.py. The library is simply compiled using gcc and then imported
into the python file.

The following line shows how to compile the driver library.

``` cmake
gcc --std=gnu11 -shared -fPIC io.c elev.c -o driver.so /usr/lib/libcomedi.so
```
The file elev.py makes two functions available, ```go_to_floor``` and
```check_buttons()```. These functions abstracts from the elevator driver,
and provide an easy to use interface for elevator control.

## Plan

### Network module
The network module is implemented using a master-client configuration.
The master employs a process-pair technique to keep a backup of itself.
The following figure shows the normal situation.

![master-client](/diagrams/master-client.png)

If the master were to lose connection with the network the backup takes
over, reestablishes the connection to all the clients and creates a new
backup of itself, as shown in the figure below.

![backup-client](/diagrams/backup-client.png)

For communication between master and client we employ TCP, and we use
JSON for serialization.

### Queue module
The queue module is run on the master, and is at all times aware of the
positions, states and requests of all the elevators. When a new request is
made at a client, the client notifies the queue/master and the queue designates
the most suited elevator to fulfill the request.

### Cost function
The cost function calculates the minimum travel time.


#Project in TTK4145

## Why object oriented

##Implementation
The system is divided into a series of modules:
- Driver
- Network
- Master
- Elevator
- States


### Driver module
We use the driver interface provided and interface with it using ctypes.
A simple example is shown in example.py. The library is simply compiled using gcc
and then imported into the python file.

The following line shows how to compile the driver library.

``` cmake
gcc --std=gnu11 -shared -fPIC io.c elev.c -o driver.so /usr/lib/libcomedi.so
```

### Network module
The network module is setup in a master-client configuration. The network module on the server side is based on the SocketServer module shipped with python. Client side we have implemented a class `Client` which handles the receiving, sending and parsing of messages to the server.

The SocketServer module sets up a threaded TCPServer, and we encode the messages sent between server and client with JSON.

When a new client connects to the server a `Clienthandler` object is generated. The clienthandler is responsible for handling communication with that specific client, and passes information up to the server and master.

The following figure shows the typical situation.

![master-client](/diagrams/master-client.png)

Here each of the node controls an elevator in addition to their other responsebilities. When an internal button is pressed clientside, the client sends the master its new queue. If an external button is pressed the client notifies the master, and the master delegates the task to the most suited elevator as well as noting that the request was external.  

Every client is aware of the backup address, so that if the master loses connection, every client will reconnect to the backup, and the backup resumes the master responsebilities.

![backup-client](/diagrams/backup-client.png)

### Master module
The master module is at all times aware of the positions, states and requests of all elevators. When a new request is made at a client, the client notifies the master and the master designates the most suited elevator to fulfill the request.

Upon initiation the master module starts a UDP broadcaster in a separate thread. It is this broadcaster that the clients listen for when initiating.


#### Cost function
To determine which elevator is the fastest/best for external requests the master employes a cost function. The cost function is based on the estimated travel time for each elevator, and takes into account the number stops, distance from destination and current direction. 

### Elevator module


### States module

## Robustness

TODO: Handle loss of motor/power
TODO: If an elevator is disconnected, and reconnects at a later time, it should regain its orders.

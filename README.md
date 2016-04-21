#Project in TTK4145


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

### Master module
The master module is at all times aware of the positions, states and requests of all elevators. When a new request is made at a client, the client notifies the master and the master designates the most suited elevator to fulfill the request.

The server is instantiated as an object under the master class.

Upon initiation the master module starts a UDP broadcaster in a separate thread. It is this broadcaster that the clients listen for when initiating.

#### Cost function
To determine which elevator is the fastest/best for external requests the master employes a cost function. The cost function is based on the estimated travel time for each elevator, and takes into account the number stops, distance from destination and current direction. 

### Elevator module
When a elevator object is created it does very little. It is not until the run method is called that a connection to the server is made, and movement- and button handlers are started. The reason for this is that the master keeps a list of elevator objects, that mirror the elevator object client side.

### States module
The state module is a set of functions consisting of while loops that handle the task for an elevator in a certain state. 

## Robustness
### Network
#### Master disconnect
In case of a master disconnect there is a slave designated by the master as backup, that all other clients know the IP of. Thus, if a client loses connection to the server it will try to reconnect with the backup.
If a connection to the backup is made, the client will send a message to its new master and inform it of current position as well as the current task stack.
If connecting to the backup fails as well the elevator will enter a `single elevator mode`. This means that all orders are handled locally. 

#### Slave disconnect
External orders are distributed to the other elevators. Master marks the elevator as disconnected. Command buttons on the disconnected elevators still work.

#### Backup disconnect
If a master notices that a backup has gone unresponsive it will designate a new backup and notify the other clients 

#### Reconnection
If an elevator loses connection to the network, it will enter a `single elevator mode` while actively searching for a master broadcast. If a master is found, the elevator will connect as a slave regardless of previous state.

### Power-/movement loss
The master maintaines a timer for every elevator, that is reset every time an elevator takes on a new task. If the task is not completed within the designated time, the master will assume that something is wrong, and distribute the elevators tasks.


## Weaknesses
- There's no polling between master and clients, so a disconnect will go unnoticed until either the server or the client tries to send a message. 
- No robustness, other than slave disconnection, handled.

Diagrams:
- Node
- sequence init
- sequence message transmission
- Class diagrams

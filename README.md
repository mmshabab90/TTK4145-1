#Project in TTK4145
##Implementation
### Driver
The driver is implemented using ctypes. A simple example is shown in
example.py. The library is simply compiled using gcc and then imported
into the python file.

The following line shows how to compile the driver library.

``` cmake
gcc --std=c11 -shared -fPIC io.c elev.c -o driver.so /usr/lib/libcomedi.so
```

Abstractions
- Go_to_floor(floor)
  --* Close door
  --* Set direction
  --* Update floor lights as it moves
  --* Stop at destination
  --* Turn off light
  --* Open door

- check_buttons()
  --* Check cab buttons
  --* Check floor up/down buttons
  --* Turn on lights
  --* Notify queue

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

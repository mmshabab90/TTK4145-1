#+STARTUP: showstars
* Plan
** TODO Network module
*** P2P solution
*** TCP for internode communication
    A socket for receiving from the previous node, and
    a socket for transmitting to the next node.
*** Reliability built into the module
    If a node loses connection to the next node it automatically
    connects to the next-next node instead. It also informs the
    rest of the network of this change so that the needed actions
    can be made.
*** JSON for serialization
*** Init
    Node queries for IP address to next node and next-next node.
    Creates a persistent TCP connection to the next node. This is
    done for alle the nodes in the network.
** DONE Elevator driver
   CLOSED: [2016-03-04 fr. 15:22]
   Implement driver in python

* Implementation
** Driver
   The driver is implemented using ctypes. A simple example is shown in
   example.py. The library is simply compiled using gcc and then imported
   into the python file.

   The following line shows how to compile the driver library.
   #+begin_src c
gcc --std=c11 -shared -fPIC io.c elev.c -o driver.so /usr/lib/libcomedi.so
   #+end_src

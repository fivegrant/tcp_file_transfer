"""
 receive.py - TCP server that listens for a remote server to send file(s)
 Author: Five Grant (fivegrant@bennington.edu)
 Date: 4/2/2020
"""

import socket
import hashlib
import protocol
from host.host import *

def receive(address, port, buffer_size, directory):
  host_socket = Host(address, port, buffer_size)
  host_socket.download()
  host_socket.close()




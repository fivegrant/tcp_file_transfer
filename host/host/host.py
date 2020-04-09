"""
 host.py - TCP server that listens for a remote server to send file(s)
 Author: Five Grant (fivegrant@bennington.edu)
 Date: 4/2/2020
"""

import socket
import hashlib
import protocol
import host.host_socket

def receive(address, port, buffer_size, directory):
  host = Host(address, port, buffersize)
  host.download()
  host.save(directory)




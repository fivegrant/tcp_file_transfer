#!/usr/bin/env python3

"""
 host.py - TCP server that listens for a remote server to send file(s)
 Author: Five Grant (fivegrant@bennington.edu)
 Date: 4/2/2020
"""

import socket
import hashlib

TCP_CONFIG = {  "address":      "127.0.0.1"
             ,  "port":         1134
             ,  "buffer_size":  1000 
             }

# Setup Server
host = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host.bind((TCP_CONFIG["address"], TCP_CONFIG["port"]))
host.listen(1)

# Connect to client.py
host.accept() = connection, client_address

# Reject if bad connection

# Download files if good connection 

# Exit 
connection.close();




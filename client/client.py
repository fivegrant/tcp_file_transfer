#!/usr/bin/env python

import socket

def connect(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock

# top level exported function
def send(ip, port, buffer_size):
    sock = connect(ip, port)


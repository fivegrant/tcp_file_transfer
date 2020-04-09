#!/usr/bin/env python

import socket
from protocol import *
from struct import pack
from struct import unpack

class Client:
    def __init__(self, ip, port, buffer):
        self.socket = connect(ip, port)
        self.buffer = buffer

    def connect(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return sock

    def handshake():
        self.socket.send(messages.pack(HANDSHAKE))
        response = messages.unpack(self.socket.recv(buffer));
        if response != CONN_SUCCESS:
            raise Exception("Handshake failed.")

    def start():
        self.handshake()
        self.socket.send(messages.pack(BEGIN_SEND))

    def end():
        self.socket.send(messages.pack(END_SEND))

    def upload(file):
        self.socket.send(messages.pack(BEGIN_FILE))


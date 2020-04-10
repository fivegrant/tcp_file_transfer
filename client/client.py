#!/usr/bin/env python

import socket
from protocol import *
from struct import pack
from struct import unpack

class Client:
    def __init__(self, ip, port, buffer_size):
        self.socket = connect(ip, port)
        self.buffer_size = buffer_size

    def connect(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return sock

    def handshake(self):
        self.socket.send(messages.pack(HANDSHAKE))
        response = messages.unpack(self.socket.recv(self.buffer_size));
        if response != CONN_SUCCESS:
            raise Exception("Handshake failed.")

    def start(self):
        self.handshake()
        self.socket.send(messages.pack(BEGIN_SEND))

    def end(self):
        self.socket.send(messages.pack(END_SEND))

    def upload(self, filename):
        self.socket.send(messages.pack(BEGIN_FILE))
        meta = metadata.pack(filename);
        self.socket.send(meta)
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(self.buffer_size), b""):
                self.socket.send(chunk)
    

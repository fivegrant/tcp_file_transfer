#!/usr/bin/env python

import socket
from protocol import *
from struct import pack
from struct import unpack

class Client:
    def __init__(self, ip, port, buffer_size):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = buffer_size
        self.ip = ip
        self.port = port

    def handshake(self):
        self.sock.connect((self.ip, self.port))
        self.sock.send(messages.pack(HANDSHAKE))
        response = messages.unpack(self.sock.recv(self.buffer_size))[0]
        if response != CONN_SUCCESS:
            raise Exception("Handshake failed.")

    def start(self):
        self.handshake()
        self.sock.send(messages.pack(BEGIN_SEND))

    def end(self):
        self.sock.send(messages.pack(END_SEND))

    def upload(self, filename):
        self.sock.send(messages.pack(BEGIN_FILE))
        meta = pack_metadata(filename)
        self.sock.send(meta)
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(self.buffer_size), b""):
                self.sock.send(chunk)
    

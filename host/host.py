"""
 host.py - TCP server that listens for a remote server to send file(s)
 Author: Five Grant (fivegrant@bennington.edu)
 Date: 4/0/2020
"""

import socket
import hashlib
from struct import pack, unpack
from protocol import *

class Host:
  def __init__(self, address, port, buffer_size, directory):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((address, port))
    self.buffer_size = buffer_size
    self.directory = directory
    self.client = None
    self.connection = None
  
  def verify(self, check, contents):
    checksum = hashlib.md5()
    checksum.update(contents)
    if checksum.hexdigest() == check:
        return True
    else:
        return False 

  def check_buffer(self):
    return messages.unpack(self.connection.recv(self.buffer_size))[0]
    
  def handshake(self, connection_patience = 1):
    if self.connection == None:
        self.sock.listen(connection_patience)
        self.connection, self.client = self.sock.accept()
        if self.check_buffer() != HANDSHAKE: 
            self.connection.send(messages.pack(ERR_MODE))
            self.client = None
            self.connection = None
            return False
        else:
            #Confirm connection
            self.connection.send(messages.pack(CONN_SUCCESS))
            return True
    else:
        return True

  def save(self):
    stream = self.connection.recv(self.buffer_size)
    meta, content = stream[:metadata_length], stream[metadata_length:]
    #Process Metadata
    ( name_length, 
      checksum, 
      filename, 
      file_length ) = metadata.unpack(meta) 
    while len(content) != file_length:
        content += self.connection.recv(buffer_size)
        if(self.verify(checksum, content)):
            with open(self.directory + filename, 'wb') as product:
                product.write(contents)
            return True
        else:
            return False
          
  def download(self):
    if self.handshake():
        if messages.unpack(self.connection.recv(self.buffer_size)) != BEGIN_SEND:
            self.connection.send(messages.pack(ERR_MODE))
            return False

        comms = self.connection.recv(self.buffer_size)
        while messages.unpack(comms) != END_SEND:
            if messages.unpack(comms) != BEGIN_FILE:
                self.connection.send(messages.pack(ERR_MODE))
                continue
            self.save()
            comms = self.connection.recv(self.buffer_size)
        self.connection.send(messages.pack(CONN_SUCCESS))
        return True

    else:
      return False

  def close(self):
    self.client = None
    self.connection.close()
    self.connection = None


# References:
#   https://docs.python.org/3/howto/sockets.html

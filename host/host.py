"""
 host.py - TCP server that listens for a remote server to send file(s)
 Author: Five Grant (fivegrant@bennington.edu)
 Date: 4/10/2020
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
    #Clean up path
    self.directory = directory \
        if directory[-1] == "/" else directory + "/"
    self.client = None
    self.connection = None
    self.cache = b''
    #Log of all the filenames
    self.log = []

  def enqueue(self, data):
    self.cache += data

  def push(self, data):
    self.cache = data + self.cache

  def pop(self, amount):
    free, self.cache = self.cache[:amount], self.cache[amount:]
    return free

  def verify(self, check, contents):
    checksum = hashlib.md5()
    checksum.update(contents)
    if checksum.hexdigest() == check:
        return True
    else:
        return False 

  def receive(self, size = 0, structure = messages, raw = False):
    size = self.buffer_size if not size else size
    self.enqueue(self.connection.recv(size))
    stream = self.pop(size)
    if not raw:
        message = structure.unpack(stream)
        return message[0] if len(message) == 1 else message
    else:
        return stream
    
  def send(self, message):
    return self.connection.send(messages.pack(message))

  def handshake(self, connection_patience = 1):
    if self.connection == None:
        self.sock.listen(connection_patience)
        self.connection, self.client = self.sock.accept()
        if self.receive(1) != HANDSHAKE: 
            self.send(ERR_MODE)
            self.close()
            return False
        else:
            #Confirm connection
            self.send(CONN_SUCCESS)
            return True
    else:
        return True

  def save(self):
    #Process Metadata
    ( name_length, 
      checksum, 
      filename, 
      file_length ) = self.receive(metadata_length, metadata) 
    filename = filename.decode()[:name_length]
    checksum = checksum.decode()
    content = b''
    while len(content) < file_length:
        content += self.receive(raw=True)
    content, remaining = content[:file_length], content[file_length:]
    self.push(remaining)
    if(self.verify(checksum, content)):
        name = f"{self.directory}{filename}"
        with open(name, 'wb') as product:
            product.write(content)
        self.log += [name]
        return self.receive(1)
    else:
        return ERR_MODE
          
  def download(self):
    if self.handshake():
        if self.receive(1) != BEGIN_SEND:
            self.send(ERR_MODE)
            return False
        comms = self.receive(1)
        while comms != END_SEND:
            if comms != BEGIN_FILE:
                self.send(ERR_MODE)
                continue
            comms = self.save()
        self.send(CONN_SUCCESS)
        return True
    else:
      return False

  def close(self):
    self.client = None
    try:
        self.connection.close()
    except AttributeError:
        pass
    self.connection = None
    return self.log


# References:
#   https://docs.python.org/3/howto/sockets.html

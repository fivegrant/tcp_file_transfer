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
    self.directory = directory if directory[-1] == "/" else directory + "/"
    self.client = None
    self.connection = None
  
  def verify(self, check, contents):
    checksum = hashlib.md5()
    checksum.update(contents)
    if checksum.hexdigest() == check:
        return True
    else:
        return False 

  def receive(self, size = 0):
    if not size:
        return messages.unpack(self.connection.recv(self.buffer_size))[0]
    else:
        return messages.unpack(self.connection.recv(size))[0]
    
  def send(self, message):
    return self.connection.send(messages.pack(message))

  def handshake(self, connection_patience = 1):
    if self.connection == None:
        self.sock.listen(connection_patience)
        self.connection, self.client = self.sock.accept()
        if self.receive() != HANDSHAKE: 
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
    stream = self.connection.recv(self.buffer_size)
    meta, content = stream[:metadata_length], stream[metadata_length:]
    #Process Metadata
    ( name_length, 
      checksum, 
      filename, 
      file_length ) = metadata.unpack(meta) 
    filename = filename.decode()[:name_length]
    checksum = checksum.decode()
    while len(content) != file_length:
        content += self.connection.recv(self.buffer_size)
        content, response = content[:file_length], content[file_length:]
        if(self.verify(checksum, content)):
            with open(f"{self.directory}{filename}", 'wb') as product:
                product.write(content)
            return messages.unpack(response)[0]
        else:
            return ERR_MODE
          
  def download(self):
    if self.handshake():
        if self.receive() != BEGIN_SEND:
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


# References:
#   https://docs.python.org/3/howto/sockets.html

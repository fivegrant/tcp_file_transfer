import socket
import hashlib
from protocol import *

class Host:
  def __init__(self, address, port, buffer_size):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((address, port))
    self.buffer_size = buffer_size
    self.client = None
    self.connection = None
    self.files = []
  
  def handshake(self, connection_patience = 1):
    if connection == None:
        self.sock.listen(connection_patience)
        self.connection, self.client = self.sock.accept()
        stream = self.connection.recv(1)
        if stream.decode() != HANDSHAKE: 
            self.sock.send(ERR_MODE.encode())
            self.client = None
            self.connection = None
            return False
        else:
            #Confirm connection
            self.sock.send(CONN_SUCCESS.encode())
            return True
    else:
        return True

  def download(self, connection_patience = 1):
    if self.handshake():
      comms = self.connection.recv(1)
      if meta.decode() != BEGIN_SEND:
        host.send(ERR_MODE.encode())
        return False

      comms = self.connection.recv(1)
      while comms.decode() != END_SEND:
        if comms.decode() != BEGIN_FILE:
          host.send(ERR_MODE.encode())
          continue

        name_length = int(self.connection.recv(buffer_size).decode())
        checksum = int(self.connection.recv(buffer_size).decode())
        filename = self.connection.recv(name_length).decode() # I dont like this

        process = ""
        stream = self.connection.recv(buffer_size).decode()
        while stream.decode() != END_FILE:
          process += stream.decode()  
          stream = self.connection.recv(buffer_size).decode()

        self.files += [(filename, process, checksum)]  
        comms = self.connection.recv(buffer_size).decode()

      host.send(CONN_SUCCESS.encode())

      self.client = None
      self.connection.close()
      self.connection = None
      return True

    else:
      return False

  def save(self, directory):
    for f in self.files:
      checksum = hashlib.md5()
      checksum.update(f[1])
      if checksum.hexdigest() == f[2]:
        with open(directory + f[0], 'wb') as product:
          product.write(f[1])
        self.files.remove(f)
          



# References:
#   https://docs.python.org/3/howto/sockets.html

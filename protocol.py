"""
 protocol.py - A set of dictionaries that make interfacing with
               protocol easier.
 Authors: Five Grant (fivegrant@bennington.edu)
          Satchel Baldwin (satchelbaldwin@bennington.edu)
 Date: 4/9/2020
"""

import struct
import os
import hashlib

# messages
HANDSHAKE    = 0x01
BEGIN_SEND   = 0x02 
END_SEND     = 0x03
BEGIN_FILE   = 0x10
CONN_SUCCESS = 0xf0

# errors
ERR_MODE     = 0xF1
ERR_FILENAME = 0xF2

# one byte -- 0x00-0xFF
messages = struct.Struct('B')
# one byte (filename length) 0 to 255;
# one 32-char md5 hexdigest
# 32 bytes allocated for filename
# unsigned long for filesize
metadata = struct.Struct("B32s32sQ")
metadata_length = 80

def pack_metadata(filename):
  length = len(filename)
  if length > 32:
    raise Exception("Filename too big.")
  size = os.stat(filename).st_size
  md5 = hashlib.md5()
  with open(filename, 'rb') as file:
    for chunk in iter(lambda: file.read(4096), b""):
      md5.update(chunk)
  hexdigest = md5.hexdigest()
  return metadata.pack(length, hexdigest.encode(), filename.encode(), size)

# References:
# https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file

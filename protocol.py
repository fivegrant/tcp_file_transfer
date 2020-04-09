#!/usr/bin/env python
"""
 protocol.py - A set of dictionaries that make interfacing with
               protocol easier.
 Authors: Five Grant (fivegrant@bennington.edu)
          Satchel Baldwin (satchelbaldwin@bennington.edu)
 Date: 4/9/2020
"""

import struct

# messages
HANDSHAKE    = 0x01
BEGIN_SEND   = 0x02 
END_SEND     = 0x03
BEGIN_FILE   = 0x10
END_FILE     = 0x20
CONN_SUCCESS = 0xf0

# errors
ERR_MODE     = 0xF1
ERR_FILENAME = 0xF2

messages = struct.Struct('B')
checksum = struct.Struct("q")
#!/usr/bin/env python

"""
 protocol.py - A set of dictionaries that make interfacing with
               protocol easier.
 Author: Five Grant (fivegrant@bennington.edu)
 Date: 4/2/2020
"""
#DEVELOPMENT: THIS MODULE MAY BE REMOVED LATER IF NOT NECESSARY

# rationale: magic strings as constants is okay
#   but consider redundant calls to encode/decode instead of
#   leaving the constant as-is and using those for human-facing
#   messages like errors; benefit to naming is if we ever need
#   to change the exact hex values that this would be much easier
#   as there'd only be one copy
# -s 4/6

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

# swap semantics to human readable names for errors
# -s
decode = { HANDSHAKE:    "handshake"
         , BEGIN_SEND:   "send"
         , END_SEND:     "end"
         , BEGIN_FILE:   "bof"
         , END_FILE:     "eof"
         , CONN_SUCCESS: "success"
         , ERR_MODE:     "ERROR: Modal mismatch between client and server"
         , ERR_FILENAME: "ERROR: Bad filename (non ascii text or filename > 256 chars)"
         }

# convert socket data to readable string
def identify(value):
  try:
    return protocol.decode[hex(int(value.decode(), 16))]
  else:
    return "not part of the protocol"



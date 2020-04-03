"""
 protocol.py - A set of dictionaries that make interfacing with
               protocol easier.
 Author: Five Grant (fivegrant@bennington.edu)
 Date: 4/2/2020
"""
#DEVELOPMENT: THIS MODULE MAY BE REMOVED LATER IF NOT NECESSARY

decode = { 0x01: "handshake"
         , 0x02: "send"
         , 0x03: "end"
         , 0x10: "bof"
         , 0x20: "eof"
         , 0xF0: "success"
         , 0xF1: "modal mismatch"
         , 0xF2: "bad filename"
         }

# Swap key: value -> value: key
encode = { word : hexcode for (hexcode, word) in decode.items() }

         

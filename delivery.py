#!/usr/bin/env python3
"""
 delivery.py - Starts a TCP client or server to transer file
 Authors: Five Grant (fivegrant@bennington.edu)
          Satchel Baldwin (satchelbaldwin@bennington.edu)
 Date: 4/10/2020
"""

import argparse
import sys
from host.host import Host
from client.client import Client

PORT = 41210
BUFFER_SIZE = 2048 

argparser = argparse.ArgumentParser(prog="DELIVERY.PY", description = "Simple TCP filesharing program.")
mode = argparser.add_subparsers(required=True, help="mode help", dest="mode")

send = mode.add_parser("send", help="Send files.")
send.add_argument("ip", help="Address to send to ", type=str)
send.add_argument("file", help="File(s) to send", nargs="*")
send.set_defaults(mode="send")

receive = mode.add_parser("receive", help="Receive files.")
receive.add_argument("ip", help="Address to host on", type=str)
receive.add_argument("directory", help="Directory to download to", type=str)
receive.set_defaults(mode="receive")

args = argparser.parse_args()

if args.mode == "send":
    client = Client(args.ip, PORT, BUFFER_SIZE)
    client.start()
    for f in args.file:
        client.upload(f)
    client.end()
    sys.exit(f"Sent {', '.join(args.file)}")

if args.mode == "receive":
    host = Host(args.ip, PORT, BUFFER_SIZE, args.directory)
    host.download()
    files = host.close()
    sys.exit(f"Downloaded {', '.join(files)}")

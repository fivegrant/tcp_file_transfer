#!/usr/bin/env python
import argparse
import sys
from host.host import Host
from client.client import Client

PORT = 41210
BUFFER_SIZE = 2048 

argparser = argparse.ArgumentParser(description = "Simple TCP filesharing program.")
mode = argparser.add_mutually_exclusive_group(required=True)
mode.add_argument("-s", "--send", help="Send files.", action="store_true")
mode.add_argument("-r", "--receive", help="Receive files.", action="store_true")
argparser.add_argument("ip", help="Host or client to connect to.", type=str)
argparser.add_argument("path", help="Path to files to share or directory to receive.", nargs="*")
args = argparser.parse_args()

if not (args.send or args.receive):
    sys.exit("Must choose to send (-s) or receive (-r).")

if args.send:
    client = Client(args.ip, PORT, BUFFER_SIZE)
    client.start()
    for f in args.path:
        client.upload(f)
    client.end()

if args.receive:
    host = Host(args.ip, PORT, BUFFER_SIZE, args.path[0])
    host.download()
    host.close()

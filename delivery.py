#!/usr/bin/env python
import argparse
import sys
from host.host import Host
from client.client import Client


PORT = 41210
BUFFER_SIZE = 2048 

argparser = argparse.ArgumentParser(description = "Simple TCP filesharing program.")
send = argparser.add_argument_group()
receive = argparser.add_argument_group()
send.add_argument("-s", "--send", help="Send files.", action="store_true")
receive.add_argument("-r", "--receive", help="Receive files.", action="store_true")
argparser.add_argument("ip", help="Host or client to connect to.", type=str)
send.add_argument("files", help="Files to share.", nargs="*")
receive.add_argument("directory", help="Destination for files.", nargs="*")
args = argparser.parse_args()

if not (args.send or args.receive):
    sys.exit("Must choose to send (-s) or receive (-r).")

if args.send:
    client = Client(args.ip, PORT, BUFFER_SIZE)
    client.start()
    for f in args.files:
        client.upload(f)
    client.end()

if args.receive:
    host = Host(args.ip, PORT, BUFFER_SIZE, args.directory)
    host.download()
    host.close()

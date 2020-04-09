#!/usr/bin/env python
import argparse
import sys

argparser = argparse.ArgumentParser(description = "Simple TCP filesharing program.")
mode = argparser.add_mutually_exclusive_group()
mode.add_argument("-s", "--send", help="Send files.", action="store_true")
mode.add_argument("-r", "--receive", help="Receive files.", action="store_true")
argparser.add_argument("ip", help="Host or client to connect to.", type=str)
argparser.add_argument("files", help="Files to share.", nargs="*")
args = argparser.parse_args()

if not (args.send or args.receive):
    sys.exit("Must choose to send or receive.")

if args.send:
    # host things
    pass

if args.receive:
    # client things
    pass
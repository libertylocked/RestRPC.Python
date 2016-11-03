#!/usr/bin/python
import argparse
import sys
import rrpc


def main():
    # Parse CLI args
    parser = argparse.ArgumentParser(description="RRPC service for Python")
    parser.add_argument("-s", required=True, help="Server URI")
    parser.add_argument("-n", required=True, help="Service name")
    parser.add_argument("-u", required=True, help="Username for HTTP auth")
    parser.add_argument("-p", required=True, help="Password for HTTP auth")

    args = parser.parse_args()

    func_dict = {"echo":echo, "print":print_to_screen}
    ws = rrpc.new_rrpc_ws(args.n, args.s, args.u, args.p, func_dict)
    ws.run_forever()


def echo(args):
    return args


def print_to_screen(args):
    print args
    return True


if __name__ == "__main__":
    main()

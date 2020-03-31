"""Main file for running program"""

import argparse
import logging
import os

from pcap2ip import Pcap2IP
from ip2map import IP2Map


def log_function():
    """Instantiate logger"""

    LOG = "message-log.log"

    # Clear log if it already exists
    if os.path.exists(LOG):
        os.remove(LOG)

    # Instantiate logger, include timestamp
    FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'
    logging.basicConfig(filename='message-log.log',
                        level=logging.DEBUG,
                        format=FORMAT)


def get_filename():
    """Get filename via argparse"""

    parser = argparse.ArgumentParser(description="Map IP's from .pcap")
    parser.add_argument('filename', metavar='file', type=str,
                        help='.pcap file name ')
    args = parser.parse_args()

    return args.filename


def is_pcap(filename):
    """Check that file is pcap. Return error if not"""

    # Check that pcap is used as input
    file_ending = filename.split(".")[-1]
    if "pcap" not in file_ending:
        raise ValueError("File must be a .pcap")


if __name__ == "__main__":

    # Instantiate logger
    log_function()

    # Get filename of .pcap to process
    FILE = get_filename()

    # Check that input file is .pcap
    is_pcap(FILE)

    # Get IPs, map it, output map
    iplist = Pcap2IP(FILE).ips
    ip2map = IP2Map(iplist)
    ip2map.coord2map()

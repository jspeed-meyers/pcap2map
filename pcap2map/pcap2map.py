"""Main file for running program"""

import argparse
import logging
import os
from pathlib import Path

from pcap2ip import Pcap2IP
from ip2map import IP2Map

# TODO: Add class and make sure
# that after downloading from pypi test
# this class and be accessed one can
# run the pipeline
# TODO: Add cli argument for location of
# final png - modify get_filename

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


def get_args():
    """Get command line arguments via argparse"""

    parser = argparse.ArgumentParser(description="Map IP's from .pcap")
    parser.add_argument('filename', metavar='file', type=str,
                        help='.pcap file name')
    parser.add_argument('--png_path', metavar='png_path', type=str,
                        help='Final path for PNG map')
    args = parser.parse_args()

    return args.filename, args.png_path


def png_path(FILE, PNG_PATH):
    """Determine correct path for final png of map"""
    
    # Cross-platform approach to getting filename stem
    file_stem = Path(FILE).stem

    # If no path specified, place in images folder
    if PNG_PATH is None:
        # TODO: Make this platform-agnostic with PATH
        png_file_name = "images/ip_map_" + file_stem + ".png"
    else:  # Otherwise place in specified folder
        # TODO: Make this platform-agnostic with PATH
        png_file_name = PNG_PATH +  file_stem + ".png"

    return png_file_name


def is_pcap(filename):
    """Check that file is pcap. Return error if not"""

    # Check that pcap is used as input
    file_ending = filename.split(".")[-1]
    if "pcap" not in file_ending:
        raise ValueError("File must be a .pcap")


if __name__ == "__main__":

    # Instantiate logger
    log_function()

    # Get arguments from command line
    FILE, PNG_PATH = get_args()
    print(PNG_PATH)

    # Determine correct path for final PNG
    PNG_PATH = png_path(FILE, PNG_PATH)

    # Check that input file is .pcap
    is_pcap(FILE)

    # Get IPs, map it, output map
    iplist = Pcap2IP(FILE).ips
    ip2map = IP2Map(iplist)
    ip2map.coord2map()

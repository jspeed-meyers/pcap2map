"""Main file for running program"""

import argparse
import logging
import os
from pathlib import Path

from pcap2ip import Pcap2IP
from ip2map import IP2Map


class Pcap2Map():

    def __init__(self):
        self.file = None
        self.png_path = None


    def run(self, file, png_path):

        # Instantiate logger
        self.log_function()

        # Get arguments from command line
        if self.file is None:
            self.file, self.png_path = self.get_args()
        else:
            self.file, self.png_path = file, png_path

        # Determine correct path for final PNG
        PNG_PATH = self.png_path_func(self.file, 
                                      self.png_path)

        # Check that input file is .pcap
        self.is_pcap(self.file)

        # Get IPs, map it, output map
        iplist = Pcap2IP(self.file).ips
        ip2map = IP2Map(iplist)
        ip2map.coord2map(PNG_PATH)


    def log_function(self):
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


    def get_args(self):
        """Get command line arguments via argparse"""

        parser = argparse.ArgumentParser(prog='pcap2map',
            description="""Extract all external IP's from a network traffic
                          (.pcap) file, determine geo-coordinates with
                          database, place IP's on a world map (.png).""",
            epilog="Happy pcap'ing")
        parser.add_argument('filename', metavar='file',
                            type=str, help='.pcap file name')
        parser.add_argument('--png_path', metavar='png_path',
                            type=str, help='Final path for PNG map')
        args = parser.parse_args()

        return args.filename, args.png_path


    def png_path_func(self, FILE, PNG_PATH):
        """Determine correct path for final png of map"""
        
        # Cross-platform approach to getting filename stem
        file_stem = Path(FILE).stem
        full_stem = "ip_map_" + file_stem + ".png"
        # If no path specified, place in images folder
        if PNG_PATH is None:
            png_file_name = os.path.join('images',
                                         full_stem)
        else:  # Otherwise place in specified folder
            png_file_name = os.path.join(PNG_PATH,
                                        'images',
                                         full_stem)

        return png_file_name


    def is_pcap(self, filename):
        """Check that the file is a pcap. Return error if not"""

        # Check that pcap is used as input
        suffixes_list = Path(filename).suffixes
        if ".pcap" not in suffixes_list:
            raise ValueError("File must be a .pcap")


if __name__ == "__main__":

    pcap2map = Pcap2Map()

    # Get command line arguments
    FILE, PNG_PATH = pcap2map.get_args()

    # Run main function
    pcap2map.run(FILE, PNG_PATH)

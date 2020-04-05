"""
Enable command line execution of pcap2map
"""

from pcap2map.pcap2map import Pcap2Map


if __name__ == "__main__":

    pcap2map = Pcap2Map()

    # Get command line arguments
    FILE, PNG_PATH = pcap2map.get_args()

    # Run main function
    pcap2map.run(FILE, PNG_PATH)

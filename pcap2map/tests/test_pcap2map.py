"""Testing module"""

import sys

import pcap2ip
import ip2map
import pcap2map


# TODO: Create classes for tests
# TODO: Test individual class methods

def test_pcap2ip():
    """Test entire pcap2ip pipeline"""

    test = pcap2ip.Pcap2IP("tests/test.pcap")
    assert test.ips == ['1.1.23.3', '1.1.12.1']

def test_ip2map():
    """Test entire ip2map pipeline"""

    # Set command line arguments for testing purposes
    sys.argv = ['pcap2ip.py', 'tests/test.pcap']

    ip_list_test = pcap2ip.Pcap2IP("tests/test.pcap").ips
    test = ip2map.IP2Map(ip_list_test)

    assert test.coord_list == [[23.116671, 113.25], [23.116671, 113.25]]

    test.coord2map('tests/test.png')

def test_pcap2map():
    """Test pcap2map entire pipeline"""

    # Set command line arguments for testing purposes
    sys.argv = ['pcap2map.py', 'tests/test.pcap']

    test = pcap2map.Pcap2Map()

    # Get command line arguments
    FILE, PNG_PATH = test.get_args()

    # Run main function
    test.run(FILE, PNG_PATH)



"""Testing module"""

import sys

import pcap2ip
import ip2map
import pcap2map

# TODO: Test individual class methods


class TestPcap2ip:
    """Test pipeline and functions of pcap2ip.py"""

    def test_pcap2ip(self):
        """Test entire pcap2ip pipeline"""

        test = pcap2ip.Pcap2IP("tests/test.pcap")
        assert test.ips == ['1.1.23.3', '1.1.12.1']

    def test_ingest_pcap(self):
        """Test ingest_pcap function"""

        test = pcap2ip.Pcap2IP("tests/test.pcap")
        test.ingest_pcap()

    def test_ip_list(self):
        """Test ip_list function"""

        test = pcap2ip.Pcap2IP("tests/test.pcap")
        assert test.ip_list() == ['1.1.23.3',
                                  '1.1.12.1']


class TestIP2map:
    """Test pipeline and functions of ip2map.py"""

    def test_ip2map(self):
        """Test entire ip2map pipeline"""

        # Set command line arguments for testing purposes
        sys.argv = ['pcap2ip.py', 'tests/test.pcap']

        ip_list_test = pcap2ip.Pcap2IP("tests/test.pcap").ips
        test = ip2map.IP2Map(ip_list_test)

        assert test.coord_list == [[23.116671, 113.25], [23.116671, 113.25]]

        test.coord2map('tests/test.png')

    def test_ip2coord(self):
        """Test ip2coord function"""

        # Set command line arguments for testing purposes
        sys.argv = ['pcap2ip.py', 'tests/test.pcap']

        ip_list_test = pcap2ip.Pcap2IP("tests/test.pcap").ips
        test = ip2map.IP2Map(ip_list_test)

        assert test.ip2coord() == [[23.116671, 113.25], 
                                   [23.116671, 113.25]]

    def test_coord2map(self):
        """Test coord2map function"""

        # Set command line arguments for testing purposes
        sys.argv = ['pcap2ip.py', 'tests/test.pcap']

        ip_list_test = pcap2ip.Pcap2IP("tests/test.pcap").ips
        test = ip2map.IP2Map(ip_list_test)

        test.coord2map('tests/test.png')


class TestPcap2Map:

    def test_pcap2map():
        """Test pcap2map entire pipeline"""

        # Set command line arguments for testing purposes
        sys.argv = ['pcap2map.py', 'tests/test.pcap']

        test = pcap2map.Pcap2Map()

        # Get command line arguments
        FILE, PNG_PATH = test.get_args()

        # Run main function
        test.run(FILE, PNG_PATH)

    def function():
        pass



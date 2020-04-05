"""Testing module"""

import os
import sys

import pytest

import pcap2ip
import ip2map
import pcap2map.pcap2map  as pcap2map # import Pcap2Map


class TestPcap2ip:
    """Test pipeline and functions of pcap2ip.py"""

    def test_pcap2ip(self):
        """Test entire pcap2ip pipeline"""

        input_file_arg = os.path.join('tests', 'test.pcap')
        test = pcap2ip.Pcap2IP(input_file_arg)
        assert test.ips == ['1.1.23.3', '1.1.12.1']

    def test_ingest_pcap(self):
        """Test ingest_pcap function"""

        input_file_arg = os.path.join('tests', 'test.pcap')
        test = pcap2ip.Pcap2IP(input_file_arg)
        test.ingest_pcap()

    def test_ip_list(self):
        """Test ip_list function"""

        input_file_arg = os.path.join('tests', 'test.pcap')
        test = pcap2ip.Pcap2IP(input_file_arg)
        assert test.ip_list() == ['1.1.23.3',
                                  '1.1.12.1']


class TestIP2map:
    """Test pipeline and functions of ip2map.py"""

    def test_ip2map(self):
        """Test entire ip2map pipeline"""

        # Set command line arguments for testing purposes
        input_file_arg = os.path.join('tests', 'test.pcap')
        sys.argv = ['pcap2ip.py', input_file_arg]

        ip_list_test = pcap2ip.Pcap2IP(input_file_arg).ips
        test = ip2map.IP2Map(ip_list_test)

        assert test.coord_list == [[23.116671, 113.25], [23.116671, 113.25]]

        PNG_PATH = os.path.join('tests', 'test.png')
        test.coord2map(PNG_PATH)

    def test_ip2coord(self):
        """Test ip2coord function"""

        # Set command line arguments for testing purposes
        input_file_arg = os.path.join('tests', 'test.pcap')
        sys.argv = ['pcap2ip.py', input_file_arg]

        ip_list_test = pcap2ip.Pcap2IP(input_file_arg).ips
        test = ip2map.IP2Map(ip_list_test)

        assert test.ip2coord() == [[23.116671, 113.25],
                                   [23.116671, 113.25]]

    def test_coord2map(self):
        """Test coord2map function"""

        # Set command line arguments for testing purposes
        input_file_arg = os.path.join('tests', 'test.pcap')
        sys.argv = ['pcap2ip.py', input_file_arg]

        ip_list_test = pcap2ip.Pcap2IP(input_file_arg).ips
        test = ip2map.IP2Map(ip_list_test)

        PNG_PATH = os.path.join('tests', 'test.png')
        test.coord2map(PNG_PATH)


class TestPcap2Map:
    """Test Pcap2Map pipeline and methods"""

    def test_pcap2map(self):
        """Test pcap2map entire pipeline"""

        # Set command line arguments for testing purposes
        input_file_arg = os.path.join('tests', 'test.pcap')
        sys.argv = ['pcap2map.py', input_file_arg]

        test = pcap2map.Pcap2Map()

        # Get command line arguments
        FILE, PNG_PATH = test.get_args()

        # Run main function
        test.run(FILE, PNG_PATH)

    def test_log_function(self):
        """Test log_function function"""

        # Set command line arguments for testing purposes
        input_file_arg = os.path.join('tests', 'test.pcap')
        sys.argv = ['pcap2map.py', input_file_arg]

        test = pcap2map.Pcap2Map()

        test.log_function()

    def test_getargs(self):
        """Test get_args function"""

        # Set command line arguments for testing purposes
        input_file_arg = os.path.join('tests', 'test.pcap')
        sys.argv = ['pcap2map.py', input_file_arg]

        test = pcap2map.Pcap2Map()
        FILE, PNG_PATH = test.get_args()

        assert FILE == os.path.join('tests',
                                    'test.pcap')
        assert PNG_PATH is None

        png_file_arg = os.path.join('tests', 'test.png')
        sys.argv = ['pcap2map.py', input_file_arg,
                    '--png_path', png_file_arg]

        test = pcap2map.Pcap2Map()
        FILE, PNG_PATH = test.get_args()

        assert FILE == os.path.join('tests', 'test.pcap')
        assert PNG_PATH == os.path.join('tests',
                                        'test.png')

    def test_png_path_func(self):
        """Test png_path function"""

        FILE = os.path.join('tests', 'test.pcap')
        PNG_PATH = None

        test = pcap2map.Pcap2Map()
        path = test.png_path_func(FILE, PNG_PATH)

        assert path == os.path.join('images',
                                    'ip_map_test.png')

        FILE = os.path.join('tests', 'test.pcap')
        PNG_PATH = 'tests'

        test = pcap2map.Pcap2Map()
        path = test.png_path_func(FILE, PNG_PATH)

        assert path == os.path.join('tests',
                                    'images',
                                    'ip_map_test.png')

    def test_is_pcap(self):
        """Test is_pcap function"""

        FILE = os.path.join('tests', 'test.pcap')
        test = pcap2map.Pcap2Map()
        test.is_pcap(FILE)

        # Check that non pcap file raises exception
        FILE = os.path.join('tests', 'test.xls')
        test = pcap2map.Pcap2Map()
        with pytest.raises(Exception):
            test.is_pcap(FILE)

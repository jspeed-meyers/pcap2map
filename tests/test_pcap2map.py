"""Testing module"""

import pcap2ip
import ip2map

# TODO: pylint
# TODO: flake8

def test_pcap2ip():
    """Test entire pcap2ip pipeline"""

    test = pcap2ip.Pcap2IP("tests/test.pcap")
    assert test.ips == ['1.1.23.3', '1.1.12.1']

def test_ip2map():
    """Test entire ip2map pipeline"""

    ip_list_test = pcap2ip.Pcap2IP("tests/test.pcap").ips
    test = ip2map.IP2Map(ip_list_test)
    
    assert test.coord_list == [[23.116671, 113.25], [23.116671, 113.25]]
    
    test.coord2map()

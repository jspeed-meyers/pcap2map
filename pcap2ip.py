""" Parse pcap for unique  IPs"""

import ipaddress

import pyshark


class Pcap2IP():
    """Pcap2IP ingests a .pcap file and creates
    a list of unique IPs.
    """

    def __init__(self, fp):
        self.fp = fp
        self.cap = self.ingest_pcap()
        self.ips = self.ip_list()

    def ingest_pcap(self):
        """Ingest pcap and convert to pyshark
        readable format
        """

        return pyshark.FileCapture(self.fp)

    def ip_list(self):
        """Ingest pyshark-readable file and output
        list of uniquqe IPs. Only include IP's that
        are public

        TODO: How does this handle IPv4 vs IPv6?
        """

        ip_list = []
        for packet in self.cap:
            src_ip = packet.ip.src
            dest_ip = packet.ip.dst

            # Check if IP's are public
            src_pub = not ipaddress.ip_address(src_ip).is_private
            dest_pub = not ipaddress.ip_address(dest_ip).is_private

            # Add IP's only if not already in list
            # and IP is public
            if src_ip not in ip_list and src_pub:
                ip_list.append(src_ip)

            if dest_ip not in ip_list and dest_pub:
                ip_list.append(dest_ip)

        return ip_list

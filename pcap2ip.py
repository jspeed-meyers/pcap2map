""" Parse pcap for unique  IPs"""

import pyshark

# TODO: create requirements.txt
# TODO: Add in testing
# Experiment with fuzzing


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
        list of uniquqe IPs

        TODO: I only want external IPs.
        TODO: How does this handle IPv4 vs IPv6?
        """

        ip_list = []
        for packet in self.cap:
            src_ip = packet.ip.src
            dest_ip = packet.ip.dst

            if src_ip not in ip_list:
                ip_list.append(src_ip)

            if dest_ip not in ip_list:
                ip_list.append(dest_ip)

        return ip_list


if __name__ == "__main__":

    # TODO: Take file as argument, not hard-coded
    test = Pcap2IP("tests/test.pcap")
    print(test.ips)

# ip-map
# Visualize geographies of IP's in map

import pyshark

# Requirements
# 1. Read in .pcap file - working
# 2. Identify all external IPs - beta

# Next stage for Wednesday night
# 3. Visualize on map all external IPs (most tools do this)
# TODO: Figure out how this 3rd component
# wants to ingest IPs

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
		TODO: Which visualization am I going to
		use? And so do I need source/dest pairs?
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

	## TODO: Take file as argument, not hard-coded
	test = Pcap2IP("sample.pcap")
	print(test.ips)



# For visualizing once I have a list
# https://github.com/pieqq/PyGeoIpMap
# https://github.com/tuxxy/ip-location-map
# https://github.com/jj09/ip-heatmap-generator
# https://github.com/ammaraskar/GeoIP-Scraper
# https://github.com/yaph/ip-location-maps
# https://github.com/jacquev6/IpMap
# https://github.com/masayuki0812/ip-country-mapping
# https://github.com/pla1/mapconnections
# https://github.com/mail-de/GeoIP-Fullsize-GoogleMaps
# https://github.com/Datamine/IP-Mapper
# https://github.com/linusg/serverlog2map
# https://github.com/cran/geoPlot
# https://github.com/scashin133/live-ip-mapper
# https://github.com/invisiblethreat/threat-vis
# https://github.com/guozheng/locviz
# https://github.com/mleewise/ip-to-map
# https://github.com/alexstocker/map2ip
# https://github.com/joergsteinkamp/maptraceroute
# https://github.com/gehuiban/ipMaps
# https://github.com/totor59/ipMap
# https://github.com/Mikkal24/IPHeatMap
# https://github.com/smulrich/IpMap

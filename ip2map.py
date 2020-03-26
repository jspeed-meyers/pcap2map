# Plot IPs on map

from pcap2ip import Pcap2IP
## TODO: See what I can rip out of this dependency
## and see what still works.
import IP2Location
 
class IP2Map():

	def __init__(self, ip_list):
		self.ip_list = ip_list
		self.coord_list = self.ip2coord()


	def ip2coord(self):
		"""Retrieve lat/long from IP

		Output:
		--A list of lists in which each
		inner list is a lat-long list
		"""

		# Access IP to coord database
		IP2LocObj = IP2Location.IP2Location()
		IP2LocObj.open("data/ip.BIN")

		# Loop thru IPs
		geo_list = []
		for ip in self.ip_list:
			# Call IP object
			rec = IP2LocObj.get_all(ip)
			# Get lat and long of IP
			lat_coord = rec.latitude
			long_coord = rec.longitude
			geo_list.append([lat_coord, long_coord])

		return geo_list

if __name__ == "__main__":

	ip_list = Pcap2IP("sample.pcap").ips
	test = IP2Map(ip_list)
	print(test.coord_list)

# TODO
# NUMBER 2. Place lat-longs on map

# perhaps geopandas
# https://geopandas.org/mapping.html

# https://github.com/ammaraskar/GeoIP-Scraper
# good map, see grey DDoS map

# google maps



# For visualizing once I have a list

# https://github.com/pieqq/PyGeoIpMap
# well documented, world map (customizable), png, free maxmind, python

# https://github.com/tuxxy/ip-location-map
# decent documentation, sparse world map, png, API subscription, python

# https://github.com/jj09/ip-heatmap-generator
# poor documentation, unclear map, unclear, unclear

# https://github.com/ammaraskar/GeoIP-Scraper
# I like their DDoS map! but uses log files to get IP. I don't like that

# https://github.com/yaph/ip-location-maps
# dots on blank space, not the type of map I'm looking for, Not what I'm looking for

# https://github.com/jacquev6/IpMap
# not a geographic map

# https://github.com/masayuki0812/ip-country-mapping
# all in bash, doesn't do mapping

# https://github.com/pla1/mapconnections
# in bash, no diagram

# https://github.com/mail-de/GeoIP-Fullsize-GoogleMaps
# Decent documentation, uses maxmind, google maps--not great

# https://github.com/Datamine/IP-Mapper
# crap maps, creates sized circles. so-so

# https://github.com/linusg/serverlog2map
# nice flask-based map and transparent dots
# but don't like the varied geography

# https://github.com/cran/geoPlot
# no documentation, unclear, r

# https://github.com/scashin133/live-ip-mapper
# javascript, unclear documentation, no map

# https://github.com/invisiblethreat/threat-vis
# unclear

# https://github.com/guozheng/locviz
# javascript

# https://github.com/mleewise/ip-to-map
# doesn't put anything on map

# https://github.com/alexstocker/map2ip
# decent map, do I want country names on my map
# javascript, not entirely clear how it works

# https://github.com/joergsteinkamp/maptraceroute
# uses perl, no image

# https://github.com/gehuiban/ipMaps
# javascript, garbage

# https://github.com/totor59/ipMap
# silly ascii art map

# https://github.com/Mikkal24/IPHeatMap
# nothing there

# https://github.com/smulrich/IpMap

# #!/usr/bin/env python
# from __future__ import print_function
# from argparse import ArgumentParser
# from contextlib import contextmanager
# from sys import stdin, stdout, stderr
# import json
# try:
#     import urllib2
# except ImportError:
#     import urllib.request as urllib2


# def memoize(func):
#     '''
#     Decorator for a function which caches results. Based on
#     http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/
#     '''
#     class memodict(dict):
#         def __missing__(self, key):
#             ret = self[key] = func(*key)
#             return ret
#         def __call__(self, *args):
#             return self[args]
    
#     return memodict()


# @memoize
# def get_location(ip):
#     print('Getting location for', ip, file=stderr)
#     url = "https://freegeoip.net/json/{}".format(ip)
#     ip_lookup = urllib2.urlopen(url)
#     ip_data = json.loads(ip_lookup.read().decode('utf-8'))
#     yield ip_data['longitude'], ip_data['latitude']

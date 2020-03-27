# Plot IPs on map

import plotly.express as px

from pcap2ip import Pcap2IP
from IP2Location import IP2Location
 
 # TODO: Add testing
 # Use pylint
 # Use flake8

class IP2Map():

	def __init__(self, ip_list):
		self.ip_list = ip_list
		self.coord_list = self.ip2coord()


	def ip2coord(self):
		"""Convert IP to lat/long

		This function uses a 3rd party module
		called IP2Location and a database in binary
		format downloaded from IP2location.com

		I don't know how accurate this database is.

		Output:
		--A list of lists in which each
		inner list is a lat-long list
		"""

		# Access IP to coord database
		IP2LocObj = IP2Location()
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

	def coord2map(self):

		# TODO: Add in functionality of taking image coordinates
		# Will need to dig into plotly
		df = px.data.gapminder().query("year == 2007")
		fig = px.scatter_geo(df, locations="iso_alpha",
                     size="pop", # size of markers, "pop" is one of the columns of gapminder
                     )
		fig.write_image("images/ip_map.png")

if __name__ == "__main__":

	ip_list = Pcap2IP("tests/test.pcap").ips
	test = IP2Map(ip_list)
	print(test.coord_list)
	test.coord2map()

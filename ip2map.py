# Plot IPs on map

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        """Place geo-coordinates of IPs on map

        Converts IP geo-cordinates list of lists into
        a pandas dataframe and then uses plotly
        to create a world map .png image with dots
        on map at proper location
    
        Returns:
        --nothing
        """
        # Convert list of IP's to pandas datframse
        df = pd.DataFrame(self.coord_list, 
                          columns=['lat', 'long'])

        # Map longitude and latitude to map dots
        fig = go.Figure(data=go.Scattergeo(
            lon = df['long'],
            lat = df['lat'],
        ))

        # Add metadata to figure
        fig.update_layout(
            title = 'Location of IPs',
            geo_scope='world',
        )

        # Save figure as .png
        fig.write_image("images/ip_map.png")

if __name__ == "__main__":

    ip_list = Pcap2IP("tests/test.pcap").ips
    test = IP2Map(ip_list)
    print(test.coord_list)
    test.coord2map()

""" Plot geocoordinates of IPs on map """

import logging
from pathlib import Path
import sys

import pandas as pd
import plotly.graph_objects as go

from IP2Location import IP2Location

# TODO: Make location of final map an optional argument
# TODO: Experiment with setup.py
# -- from where can you run ip2map.py successfully?
# Determine if setup.py is working? fix
# TODO: Experiment with dockerizing it
# TODO: Experiment with fuzzing
# TODO: Fill out readme
# TODO: Push to github
# TODO: Push to pypi
# TODO: Push to dockerhub


class IP2Map():
    """Convert IP addresses into geocoordinates and map

    IP addresses are converted into geo-coordinates
    via a 3rd party IP2Location module. These
    coordinates are then mapped with plotly.
    """

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

        logging.debug("IP geographic coordinate list: {}".format(geo_list))
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
            lon=df['long'],
            lat=df['lat'],
        ))

        # Add metadata to figure
        fig.update_layout(
            title='Location of IPs',
            geo_scope='world',
        )

        # Save figure as .png
        file_path = sys.argv[1]
        file_stem = Path(file_path).stem  # Cross-platform approach
        png_file_name = "images/ip_map_" + file_stem + ".png"
        fig.write_image(png_file_name)

""" File to simplify distributing package """

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='pcap2map',
   version='0.0.1',
   description='Put IP addresses from PCAP on map',
   author='anon',
   author_email='anon@gmail.coma',
   packages=['pcap2map'],
   classifiers=[
        "Programming Language :: Python :: 3",
    ],
   python_requires='>=3.7.6',
   install_requires=['pandas', 'plotly', 'pyshark'],
)

""" File to simplify distributing package """

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='pcap2map',
   version='0.0.4',
   description='Put IP addresses from PCAP on map',
   keywords="pcap networking IP geolocations",
   author='anon',
   author_email='anon@gmail.com',
   url="https://www.google.com",
   long_description=long_description,
   long_description_content_type="text/markdown",
   include_package_data=True,
   packages=find_packages("src"),
   package_dir={"": "src"},
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Intended Audience :: System Administrators",
        ],
   python_requires='>=3.7.6',
   install_requires=['pandas',
                     'plotly',
                     'pyshark'],
)

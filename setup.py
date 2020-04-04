""" File to simplify distributing package """

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
   name='pcap2map',
   version='0.0.1',
   description='Put IP addresses from PCAP on map',
   author='anon',
   author_email='anon@gmail.com',
   long_description=long_description,
   long_description_content_type="text/markdown",
   packages=setuptools.find_packages(),
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Intended Audience :: System Administrators"],
   python_requires='>=3.7.6'
)

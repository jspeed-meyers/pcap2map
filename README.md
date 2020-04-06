# pcap2map
### Place IP's from PCAP on world map

This package enables a user to specify a network traffic file (i.e. a packet capture or .pcap file), extract the IP addresses from that file, geo-locate those addresses using a built-in database, and then place those IP's on a world map (a .png file).

Notes:
* The geolocation is done via a database provided by IP2Location.com. The database is included as part of the package.
* Only public IP's are extracted
* Typical runtime is 10 seconds for a small .pcap file
* There are many pre-existing packages that geo-locate IP's but none that extract IP's from a .pcap. pcap2map solves the latter problem
* pcap2map was written to be cross-platform

Dependencies:
* Tshark - point to URL and installation instructions

## Installation instructions

via github:
```
git clone [url]
pip install -r requirements.txt
```

via PYPI:
```
pip install pcap2map
```

via docker:
```

```

## Usage instructions

after dowloading from github:
```
cd pcap2map\src\pcap2map
pcap2map.py [filepath\filename]
```

after downloading from pip:
```
python -m pcap2map -h  # for help
python -m pcap2map [filename]
```

after downloading from docker:
```

```

## Run tests

after downloading from github:
```
cd pcap2map\pcap2map
pytest
```

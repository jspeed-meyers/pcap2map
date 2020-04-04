# pcap2map
### Place IP's from PCAP on world map

[[pcap2map\images\ip_map_test_ipv6.png]]

This package enables a user to specify a network traffic file (i.e. a packet capture or .pcap file), extract the IP addresses from that file, geo-locate those addresses using a built-in database, and then place those IP's on a world map (a .png).

Notes:
-Only public IP's are extracted.
-Typical runtime is 10 seconds for a small .pcap
-The geolocation is done via a database provided by IP2Location.com
-There are many pre-existing packages that geo-locate IP's but none that extract IP's from a .pcap. pcap2map solves the latter problem
-pcap2map was written to be cross-platform

## Installation instructions

via git:
```
git clone [url]
pip install -r requirements.txt
```

## Usage instructions
```
cd pcap2map\pcap2map
pcap2map.py [filepath\filename]
```

## Run tests
```
cd pcap2map\pcap2map
pytest
```

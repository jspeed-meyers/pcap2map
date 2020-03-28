"""Convert IP to geolocation

Much of the functionality has been stripped out to avoid
potential security issues and make maintenance easier.

"This site or product includes IP2Location LITE data available
from http://www.ip2location.com."
Copyright (C) 2005-2016 IP2Location.com
# All Rights Reserved
"""

# Ignore line too long flake8 errors

# noqa: E501

import sys
import struct
import socket


def u(x):
    if isinstance(x, bytes):
        return x.decode()
    return x


def b(x):
    if isinstance(x, bytes):
        return x
    return x.encode('ascii')


class IP2LocationRecord:
    ''' IP2Location record with all fields from the database '''

    latitude = None
    longitude = None

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)


MAX_IPV4_RANGE = 4294967295
MAX_IPV6_RANGE = 340282366920938463463374607431768211455

_COUNTRY_POSITION = (0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
_LATITUDE_POSITION = (0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)
_LONGITUDE_POSITION = (0, 0, 0, 0, 0, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6)


class IP2Location(object):
    ''' IP2Location database operations '''

    def __init__(self, filename=None, mode='FILE_IO'):
        ''' Creates a database object and opens a file '''
        self.mode = mode
        if filename:
            self.open(filename)

    def __enter__(self):
        if not hasattr(self, '_f') or self._f.closed:
            raise ValueError("Cannot enter context with closed file")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self, filename):
        ''' Opens a database file '''

        # Ensure old file is closed before opening a new one
        self.close()

        if (self.mode == 'FILE_IO'):
            self._f = open(filename, 'rb')
        else:
            raise ValueError("Invalid mode.")

        self._dbtype = struct.unpack('B', self._f.read(1))[0]
        self._dbcolumn = struct.unpack('B', self._f.read(1))[0]
        self._dbyear = struct.unpack('B', self._f.read(1))[0]
        self._dbmonth = struct.unpack('B', self._f.read(1))[0]
        self._dbday = struct.unpack('B', self._f.read(1))[0]
        self._ipv4dbcount = struct.unpack('<I', self._f.read(4))[0]
        self._ipv4dbaddr = struct.unpack('<I', self._f.read(4))[0]
        self._ipv6dbcount = struct.unpack('<I', self._f.read(4))[0]
        self._ipv6dbaddr = struct.unpack('<I', self._f.read(4))[0]
        self._ipv4indexbaseaddr = struct.unpack('<I', self._f.read(4))[0]
        self._ipv6indexbaseaddr = struct.unpack('<I', self._f.read(4))[0]

    def close(self):
        if hasattr(self, '_f'):
            # If there is file close it.
            self._f.close()
            del self._f

    def get_latitude(self, ip):
        ''' Get latitude '''
        rec = self.get_all(ip)
        return rec and rec.latitude

    def get_longitude(self, ip):
        ''' Get longitude '''
        rec = self.get_all(ip)
        return rec and rec.longitude

    def get_all(self, addr):
        ''' Get the whole record with all fields read from the file

            Arguments:
            addr: IPv4 or IPv6 address as a string

            Returns IP2LocationRecord or None if address not found in file
        '''
        return self._get_record(addr)

    def find(self, addr):
        ''' Get the whole record with all fields read from the file

            Arguments:
            addr: IPv4 or IPv6 address as a string

            Returns IP2LocationRecord or None if address not found in file
        '''
        return self._get_record(addr)

    def _reads(self, offset):
        self._f.seek(offset - 1)
        n = struct.unpack('B', self._f.read(1))[0]
        # return u(self._f.read(n))
        if sys.version < '3':
            return str(self._f.read(n).decode('iso-8859-1').encode('utf-8'))
        else:
            return u(self._f.read(n).decode('iso-8859-1').encode('utf-8'))

    def _readi(self, offset):
        self._f.seek(offset - 1)
        return struct.unpack('<I', self._f.read(4))[0]

    def _readf(self, offset):
        self._f.seek(offset - 1)
        return struct.unpack('<f', self._f.read(4))[0]

    def _readip(self, offset, ipv):
        if ipv == 4:
            return self._readi(offset)
        elif ipv == 6:
            a, b, c, d = self._readi(offset), \
                         self._readi(offset + 4), \
                         self._readi(offset + 8), \
                         self._readi(offset + 12)

            return (d << 96) | (c << 64) | (b << 32) | a

    def _readips(self, offset, ipv):
        if ipv == 4:
            return socket.inet_ntoa(struct.pack('!L', self._readi(offset)))
        elif ipv == 6:
            return str(self._readip(offset, ipv))

    def _read_record(self, mid, ipv):
        rec = IP2LocationRecord()

        if ipv == 4:
            off = 0
            baseaddr = self._ipv4dbaddr
            dbcolumn_width = self._dbcolumn * 4 + 4
        elif ipv == 6:
            off = 12
            baseaddr = self._ipv6dbaddr
            dbcolumn_width = self._dbcolumn * 4

        def calc_off(what, mid):
            return baseaddr + mid * (self._dbcolumn * 4 + off) + off + 4 * (what[self._dbtype]-1)

        self._f.seek((calc_off(_COUNTRY_POSITION, mid)) - 1)
        raw_positions_row = self._f.read(dbcolumn_width)

        if self.original_ip != '':
            rec.ip = self.original_ip
        else:
            rec.ip = self._readips(baseaddr + (mid) * self._dbcolumn * 4, ipv)

        if _LATITUDE_POSITION[self._dbtype] != 0:
            rec.latitude = round(struct.unpack('<f', raw_positions_row[((_LATITUDE_POSITION[self._dbtype]-1) * 4 - 4): ((_LATITUDE_POSITION[self._dbtype]-1) * 4)])[0], 6)
        if _LONGITUDE_POSITION[self._dbtype] != 0:
            rec.longitude = round(struct.unpack('<f', raw_positions_row[((_LONGITUDE_POSITION[self._dbtype]-1) * 4 - 4): ((_LONGITUDE_POSITION[self._dbtype]-1) * 4)])[0], 6)

        return rec

    def __iter__(self):
        low, high = 0, self._ipv4dbcount
        while low <= high:
            yield self._read_record(low, 4)
            low += 1

        low, high = 0, self._ipv6dbcount
        while low <= high:
            yield self._read_record(low, 6)
            low += 1

    def _parse_addr(self, addr):
        ''' Parses address and returns IP version. Raises exception on invalid argument '''
        ipv = 0
        try:
            a, b = struct.unpack('!QQ', socket.inet_pton(socket.AF_INET6, addr))
            ipnum = (a << 64) | b
            # Convert ::FFFF:x.y.z.y to IPv4
            if addr.lower().startswith('::ffff:'):
                try:
                    socket.inet_pton(socket.AF_INET, addr)
                    ipv = 4
                except:
                    # reformat ipv4 address in ipv6
                    if ((ipnum >= 281470681743360) and (ipnum <= 281474976710655)):
                        ipv = 4
                        ipnum = ipnum - 281470681743360
                    else:
                        ipv = 6
            else:
                # reformat 6to4 address to ipv4 address 2002:: to 2002:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF
                if ((ipnum >= 42545680458834377588178886921629466624) and (ipnum <= 42550872755692912415807417417958686719)):
                    ipv = 4
                    ipnum = ipnum >> 80
                    ipnum = ipnum % 4294967296

                elif ((ipnum >= 42540488161975842760550356425300246528) and (ipnum <= 42540488241204005274814694018844196863)):
                    ipv = 4
                    ipnum = ~ ipnum
                    ipnum = ipnum % 4294967296
                else:
                    ipv = 6
        except:
            ipnum = struct.unpack('!L', socket.inet_pton(socket.AF_INET, addr))[0]

            ipv = 4
        return ipv, ipnum

    def _get_record(self, ip):

        # global original_ip
        self.original_ip = ip
        low = 0

        ipv = self._parse_addr(ip)[0]
        ipnum = self._parse_addr(ip)[1]
        if ipv == 4:

            if (ipnum == MAX_IPV4_RANGE):
                ipno = ipnum - 1
            else:
                ipno = ipnum
            off = 0
            baseaddr = self._ipv4dbaddr
            high = self._ipv4dbcount
            if self._ipv4indexbaseaddr > 0:
                indexpos = ((ipno >> 16) << 3) + self._ipv4indexbaseaddr
                low = self._readi(indexpos)
                high = self._readi(indexpos + 4)

        elif ipv == 6:
            if self._ipv6dbcount == 0:
                raise ValueError('Please use IPv6 BIN file for IPv6 Address.')

            if (ipnum == MAX_IPV6_RANGE):
                ipno = ipnum - 1
            else:
                ipno = ipnum
            off = 12
            baseaddr = self._ipv6dbaddr
            high = self._ipv6dbcount
            if self._ipv6indexbaseaddr > 0:
                indexpos = ((ipno >> 112) << 3) + self._ipv6indexbaseaddr
                low = self._readi(indexpos)
                high = self._readi(indexpos + 4)

        while low <= high:
            mid = int((low + high) / 2)
            ipfrom = self._readip(baseaddr + (mid) * (self._dbcolumn * 4 + off), ipv)
            ipto = self._readip(baseaddr + (mid + 1) * (self._dbcolumn * 4 + off), ipv)

            if ipfrom <= ipno < ipto:
                return self._read_record(mid, ipv)
            else:
                if ipno < ipfrom:
                    high = mid - 1
                else:
                    low = mid + 1

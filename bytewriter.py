#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""bytewriter.py: Write arrays in various ways"""

__author__ = "Aleksey.Zholdak"
__version__ = "1.0.1"
__email__ = "aleksey@zholdak.com"


class ByteAsBytearrayWriter(object):
    bytes_per_line = 16

    def __init__(self, stream, varname):
        self.stream = stream
        self.stream.write('{} = \\\n'.format(varname))
        self.bytecount = 0  # For line breaks

    def _eol(self):
        self.stream.write("'\\\n")

    def _eot(self):
        self.stream.write("'\n")

    def _bol(self):
        self.stream.write("    b'")

    # Output a single byte
    def obyte(self, data):
        if not self.bytecount:
            self._bol()
        self.stream.write('\\x{:02x}'.format(data))
        self.bytecount += 1
        self.bytecount %= self.bytes_per_line
        if not self.bytecount:
            self._eol()

    # Output from a sequence
    def out_data(self, bytelist):
        for byt in bytelist:
            self.obyte(byt)

    # ensure a correct final line
    def eot(self):  # User force EOL if one hasn't occurred
        if self.bytecount:
            self._eot()
        self.stream.write('\n')


class ByteAsIntArrayWriter(object):
    bytes_per_line = 16

    def __init__(self, stream, varname):
        self.stream = stream
        self.stream.write('{} = [\n'.format(varname))
        self.bytecount = 0  # For line breaks
        self.bytes_in_line = 0  # For line breaks

    def _eol(self):
        self.stream.write("\n")

    def _eot(self):
        self.stream.write("\n")

    def _bol(self):
        self.stream.write("    ")

    # Output a single byte
    def out_byte(self, byte):
        if self.bytecount:
            self.stream.write(',')
        if self.bytecount and not self.bytes_in_line:
            self._eol()
        if not self.bytes_in_line:
            self._bol()
        self.stream.write('{:d}'.format(byte))
        self.bytes_in_line += 1
        self.bytes_in_line %= self.bytes_per_line
        self.bytecount += 1

    # Output from a sequence
    def out_data(self, bytelist):
        for byt in bytelist:
            self.out_byte(byt)

    # ensure a correct final line
    def eot(self):  # User force EOL if one hasn't occurred
        if self.bytes_in_line:
            self._eot()
        self.stream.write(']\n')

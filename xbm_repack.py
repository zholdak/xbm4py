#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""xbm_repack.py: Adapt XBM images to use in Python"""

__author__ = "Aleksey.Zholdak"
__version__ = "1.0.1"
__email__ = "aleksey@zholdak.com"

import argparse
import os
import datetime
from bytewriter import ByteAsBytearrayWriter


def get_xbm_data(sourcefile):
    errmsg = ''.join(("File: '", sourcefile, "' is not a valid XBM file"))
    try:
        with open(sourcefile, 'r') as f:
            phase = 0
            for line in f:
                if phase < 2:
                    if line.startswith('#define'):
                        yield int(line.split(' ')[-1])
                        phase += 1
                if phase == 2:
                    start = line.find('{')
                    if start >= 0:
                        line = line[start + 1:]
                        phase += 1
                if phase == 3:
                    if not line.isspace():
                        phase += 1
                if phase == 4:
                    end = line.find('}')
                    if end >= 0:
                        line = line[:end]
                        phase += 1
                    hexnums = line.split(',')
                    if hexnums[0] != '':
                        for hexnum in [q for q in hexnums if not q.isspace()]:
                            yield int(hexnum, 16)
            if phase != 5:
                print(errmsg)
    except OSError:
        print("Can't open " + sourcefile + " for reading")


def repack_xbm(xbm_file_name, stream):
    xbm = get_xbm_data(xbm_file_name)
    width = next(xbm)
    height = next(xbm)
    stream.write("# Created by {} v{} @ {}\n".format(os.path.basename(__file__), __version__,
                                                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    stream.write("width = {:d}\n".format(width))
    stream.write("height = {:d}\n".format(height))
    writer = ByteAsBytearrayWriter(stream, "bits")
    writer.out_data(xbm)
    writer.eot()
    del writer
    del xbm


DESC = """xbm_repack.py
Utility to repack xbm images into xbm_py images.
Sample usage:
xbm_repack.py <infile.xbm> <outfile.py>
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(__file__, description=DESC, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=str, help='Input file path')
    parser.add_argument('outfile', type=str, help='Path and name of output file')
    args = parser.parse_args()

    try:
        with open(args.outfile, 'w', encoding='utf-8') as stream:
            repack_xbm(args.infile, stream)
    except OSError:
        print("Can't open", args.infile, 'for writing')

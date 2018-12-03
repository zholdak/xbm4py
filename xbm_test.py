#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""xbm_test.py: Test generated image"""

__author__ = "Aleksey.Zholdak"
__version__ = "1.0.1"
__email__ = "aleksey@zholdak.com"

from xbm_py import mmhg_xbm as xbm
from PIL import Image, ImageDraw

margin = 10
img = Image.new('L', (xbm.width + (margin * 2), xbm.height + (margin * 2)), 'white')
draw = ImageDraw.Draw(img)

byte_pos = 0
bytes_per_row = (xbm.width + 7) // 8
for row_no in range(xbm.height):
    for col_no in range(bytes_per_row):
        byte = xbm.bits[byte_pos]
        for bit_no in range(8):
            char_col_pos = bit_no + (col_no * 8)
            if char_col_pos > xbm.width:
                break
            if byte >> bit_no & 0x1:
                draw.point((char_col_pos + margin, row_no + margin))
        byte_pos += 1

img.show()
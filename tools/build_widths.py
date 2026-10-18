# -*- coding: utf-8 -*-
"""Rebuild Widths.txt: Cyrillic widths (tiles 0-65), gap (66-89), English widths shifted 0-89 -> 90-179."""
from PIL import Image

# Ink palette indices used in Font.png
INK = {1, 2, 5, 6}
img = Image.open('Font.png').convert('P')
tile = 10
nx = 16

def glyph_width(i):
    tx = (i % nx) * tile
    ty = (i // nx) * tile
    right = 0
    for y in range(tile):
        for x in range(tile):
            if img.getpixel((tx + x, ty + y)) in INK:
                if x + 1 > right:
                    right = x + 1
    return right

# Original widths (180 values in tile order) from the old Widths.txt
vals = []
for line in open('Widths.txt'):
    vals += [int(v) for v in line.split()]

assert len(vals) == 180, f"expected 180 widths, got {len(vals)}"

new = vals[:]  # keep original widths (English already at 90-179)
# Cyrillic tiles 0-65: measured width, clamped to 1..10
for i in range(66):
    w = glyph_width(i)
    new[i] = max(1, min(10, w - 1))  # compact Cyrillic to match Latin advances
# tiles 66-179: leave original (gap + English) untouched

# write 180 values, 16 per line
with open('Widths.txt', 'w') as f:
    for i in range(0, 180, 16):
        f.write(' '.join(f"{v:02d}" for v in new[i:i+16]) + '\n')

print("Widths.txt rebuilt.")
print("Cyrillic widths (tiles 0-65):", new[0:66])

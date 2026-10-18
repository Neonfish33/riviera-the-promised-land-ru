# -*- coding: utf-8 -*-
"""Rebuild IN.tbl: map Russian letters to single-byte AA-FB (tiles 0-81),
removing the broken A4/A5/A8 Cyrillic entries from the original table."""
import json, io

with open('_cyr_map.json', encoding='utf-8') as f:
    cyr = json.load(f)  # [[char, hex], ...] 66 entries

# Read original tbl preserving non-Cyrillic entries
orig_lines = io.open('Insert/IN.tbl.orig', encoding='utf-8').read().splitlines()

kept = []          # (hex, glyph) in original order
seen_hex = set()

def is_broken(hexstr):
    h = hexstr.upper()
    if h in ('A278',):  # III -> broken (tile 206)
        return True
    if h.startswith('A4') or h.startswith('A5') or h.startswith('A8'):
        return True
    return False

for line in orig_lines:
    if '=' not in line:
        continue
    hexstr, glyph = line.split('=', 1)
    hexstr = hexstr.strip().upper()
    glyph = glyph.rstrip('\r\n')  # preserve the space glyph (8A= )
    if not hexstr:
        continue
    if is_broken(hexstr):
        continue
    # skip the blank AA-FB lines; we'll fill them with Russian below
    if len(hexstr) == 2 and 0xAA <= int(hexstr, 16) <= 0xFB and not glyph:
        continue
    kept.append((hexstr, glyph))
    seen_hex.add(hexstr)

# Build output
out = []
# 1) Russian letters into AA-FB
russian_by_hex = {h: ch for ch, h in cyr}
for code in range(0xAA, 0xFC):
    h = f"{code:02X}"
    out.append(f"{h}={russian_by_hex.get(h, '')}")
# 2) everything else in original order
for hexstr, glyph in kept:
    out.append(f"{hexstr}={glyph}")

with io.open('Insert/IN.tbl', 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(out) + '\r\n')

print(f"IN.tbl rebuilt: {len(russian_by_hex)} Russian letters mapped, "
      f"{len(kept)} other entries kept.")

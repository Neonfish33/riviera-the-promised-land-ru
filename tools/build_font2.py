# -*- coding: utf-8 -*-
"""Rebuild Cyrillic tiles 0..65 in Riviera Font.png.

Style follows the original Latin tiles: 1px body strokes (palette index 6)
with an automatic 1px drop-shadow (index 2) at +1,+1.
Latin tiles 90..179 are preserved as-is.
"""
from PIL import Image
import json

img = Image.open('Font.png').convert('P')
TILE, NX = 10, 16
INK, SHADOW = 6, 2


def get_tile(i):
    tx, ty = (i % NX) * TILE, (i // NX) * TILE
    return [[img.getpixel((tx + x, ty + y)) for x in range(TILE)] for y in range(TILE)]


new = Image.new('P', (NX * TILE, 12 * TILE))
new.putpalette(img.getpalette())


def put_tile(i, pixels):
    tx, ty = (i % NX) * TILE, (i // NX) * TILE
    for y in range(TILE):
        for x in range(TILE):
            new.putpixel((tx + x, ty + y), pixels[y][x])


def glyph(rows, top):
    g = [[0] * TILE for _ in range(TILE)]
    pts = []
    for dy, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == '#':
                pts.append((x, top + dy))
    for x, y in pts:
        if x + 1 < TILE and y + 1 < TILE:
            g[y + 1][x + 1] = SHADOW
    for x, y in pts:
        if 0 <= x < TILE and 0 <= y < TILE:
            g[y][x] = INK
    return g


# keep Latin/punctuation exactly as in the current atlas
for i in range(66, 180):
    put_tile(i, get_tile(i))

# lookalikes copied from the original Latin glyphs
COPY = {
    0: 100, 2: 101, 5: 104, 8: 93, 11: 110, 13: 112, 14: 107, 15: 114,
    17: 115, 18: 102, 19: 119, 20: 124, 22: 123,
    44: 136, 47: 139, 48: 140, 50: 141, 51: 128, 53: 150, 55: 149,
}
for dst, src in COPY.items():
    put_tile(dst, get_tile(src))

# uppercase, cap rows 1..7
UP = {
    'Б': ["####", "#...", "###.", "#..#", "#..#", "#..#", "###."],
    'Г': ["####", "#...", "#...", "#...", "#...", "#...", "#..."],
    'Д': ["#####", "#...#", "#...#", "#...#", "#...#", "#...#", "##.##"],
    'Ё': ["#.#.", "####", "#...", "###.", "#...", "#...", "####"],
    'Ж': ["#.#.#", "#.#.#", ".###.", "..#..", ".###.", "#.#.#", "#.#.#"],
    'И': ["#..#", "#..#", "#.##", "##.#", "#..#", "#..#", "#..#"],
    'Й': [".##.", "#..#", "#..#", "#.##", "##.#", "#..#", "#..#", "#..#"],
    'Л': ["..##.", ".#..#", "#...#", "#...#", "#...#", "#...#", "#...#"],
    'П': ["####", "#..#", "#..#", "#..#", "#..#", "#..#", "#..#"],
    'Ф': ["..#..", "#####", "#.#.#", "#.#.#", "#####", "..#..", "..#.."],
    'Ц': ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", "#####", "....#"],
    'Ч': ["#...#", "#...#", "#...#", ".####", "....#", "....#", "....#"],
    'Ш': ["#.#.#", "#.#.#", "#.#.#", "#.#.#", "#.#.#", "#.#.#", "#####"],
    'Щ': ["#.#.#", "#.#.#", "#.#.#", "#.#.#", "#.#.#", "#.#.#", "#####", "....#"],
    'Ъ': ["##...", "#....", "###..", "#..#.", "#..#.", "#..#.", "###.."],
    'Ы': ["#...#", "#...#", "#...#", "##..#", "#.#.#", "#.#.#", "##..#"],
    'Ь': ["#....", "#....", "#....", "###..", "#..#.", "#..#.", "###.."],
    'Э': [".###.", "#...#", "....#", "..###", "....#", "#...#", ".###."],
    'Ю': ["#..##", "#.#.#", "#.#.#", "#.#.#", "#.#.#", "#.#.#", "#..##"],
    'Я': ["####.", "#...#", "#...#", "####.", "..#.#", ".#..#", "#...#"],
}

# lowercase, x-height rows 3..7 (ascenders/descenders where needed)
LO = {
    'а': ["..#", ".##", "#.#", "#.#", ".##"],
    'б': [".#.", "#..", "###", "#.#", "#.#", "#.#", "###"],
    'в': ["###", "#.#", "###", "#.#", "###"],
    'г': ["###", "#..", "#..", "#..", "#.."],
    'д': ["..#.", "..#.", ".#.#", ".#.#", "####", "...#"],
    'е': ["###", "#..", "###", "#..", "###"],
    'ё': ["#.#", "###", "#..", "###", "#..", "###"],
    'ж': ["#.#.#", ".#.#.", "..#..", ".#.#.", "#.#.#"],
    'з': ["###", "..#", ".##", "..#", "###"],
    'и': ["#..#", "#..#", "#.##", "##.#", "#..#"],
    'й': [".##.", "#..#", "#..#", "#.##", "##.#", "#..#"],
    'л': ["..##", ".#.#", "#..#", "#..#", "#..#"],
    'м': ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    'п': ["####", "#..#", "#..#", "#..#", "#..#"],
    'т': ["####", "..#.", "..#.", "..#.", "..#."],
    'ф': ["..#..", "#####", "#.#.#", "#####", "..#.."],
    'ц': ["#..#", "#..#", "#..#", "####", "...#"],
    'ч': ["#..#", "#..#", ".###", "...#", "...#"],
    'ш': ["#.#.#", "#.#.#", "#.#.#", "#.#.#", "#####"],
    'щ': ["#.#.#", "#.#.#", "#.#.#", "#.#.#", "#####", "....#"],
    'ъ': ["##..", "#...", "###.", "#..#", "###."],
    'ы': ["#...#", "#...#", "###.#", "#..##", "###.#"],
    'ь': ["#...", "#...", "###.", "#..#", "###."],
    'э': [".##.", "#..#", "..##", "#..#", ".##."],
    'ю': ["##..#", "#.#.#", "#.#.#", "#.#.#", "##..#"],
    'я': ["###.", "#..#", "###.", ".#.#", "#..#"],
}

UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

for ch in UPPER:
    t = UPPER.index(ch)
    if t in COPY:
        continue
    put_tile(t, glyph(UP[ch], 1))
for ch in LOWER:
    t = 33 + LOWER.index(ch)
    if t in COPY:
        continue
    top = 1 if ch in 'бёй' else 3
    put_tile(t, glyph(LO[ch], top))

def get_new(i):
    tx, ty = (i % NX) * TILE, (i // NX) * TILE
    return [[new.getpixel((tx + x, ty + y)) for x in range(TILE)] for y in range(TILE)]


ALIAS = {6: 5, 10: 9, 39: 38, 43: 42}  # Ё->Е, Й->И, ё->е, й->и
for dst, src in ALIAS.items():
    put_tile(dst, get_new(src))

new.save('Font.png')
print('OK: Cyrillic redrawn, copied %d, drawn %d' % (len(COPY), len(UPPER) + len(LOWER) - len(COPY)))
with open('_cyr_map.json', 'w', encoding='utf-8') as f:
    json.dump([[ch, '%02X' % (0xAA + UPPER.index(ch))] for ch in UPPER] +
              [[ch, '%02X' % (0xCB + LOWER.index(ch))] for ch in LOWER], f, ensure_ascii=False)
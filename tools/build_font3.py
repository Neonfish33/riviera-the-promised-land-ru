# -*- coding: utf-8 -*-
"""Build Cyrillic tiles from Arial Bold (pixelated at 9px), matching the
original 10x10 tile metrics: cap rows 1..7, baseline 8, shadow +1,+1."""
from PIL import Image, ImageDraw, ImageFont

SRC = 'Font.png.before_redraw'
FONT = r'C:\Windows\Fonts\arialnb.ttf'
SIZE, BASE = 9, 8
TILE, NX = 10, 16
INK, SHADOW = 6, 2

img = Image.open(SRC).convert('P')
new = Image.new('P', (NX * TILE, 12 * TILE))
new.putpalette(img.getpalette())


def get_tile(i):
    tx, ty = (i % NX) * TILE, (i // NX) * TILE
    return [[img.getpixel((tx + x, ty + y)) for x in range(TILE)] for y in range(TILE)]


def put_tile(i, px):
    tx, ty = (i % NX) * TILE, (i // NX) * TILE
    for y in range(TILE):
        for x in range(TILE):
            new.putpixel((tx + x, ty + y), px[y][x])


def glyph(ch, f):
    mask = Image.new('L', (TILE, TILE), 0)
    d = ImageDraw.Draw(mask)
    d.text((0, BASE), ch, font=f, fill=255, anchor='ls')
    body = set()
    for y in range(TILE):
        for x in range(TILE):
            if mask.getpixel((x, y)) > 110:
                body.add((x, y))
    g = [[0] * TILE for _ in range(TILE)]
    for x, y in body:
        if x + 1 < TILE and y + 1 < TILE:
            g[y + 1][x + 1] = SHADOW
    for x, y in body:
        g[y][x] = INK
    return g


for i in range(66, 180):
    put_tile(i, get_tile(i))

UP = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
LO = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALIAS = {'Ё': 'Е', 'Й': 'И', 'ё': 'е', 'й': 'и'}

f = ImageFont.truetype(FONT, SIZE)
for i, ch in enumerate(UP):
    put_tile(i, glyph(ALIAS.get(ch, ch), f))
for i, ch in enumerate(LO):
    put_tile(33 + i, glyph(ALIAS.get(ch, ch), f))

new.save('Font.png')
print('OK: TTF font built (Arial Bold %dpx)' % SIZE)

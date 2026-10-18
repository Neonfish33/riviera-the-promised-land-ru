# -*- coding: utf-8 -*-
"""Render text with the game font tiles (for visual checks)."""
from PIL import Image
import sys

img = Image.open('Font.png').convert('RGB')
TILE, NX, COLS = 10, 16, 16
UP = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
LO = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

widths = []
for line in open('Widths.txt'):
    widths += [int(v) for v in line.split()]


def tile_img(t):
    return img.crop(((t % NX) * TILE, (t // NX) * TILE,
                     (t % NX) * TILE + TILE, (t // NX) * TILE + TILE))


def char_tile(ch):
    if ch in UP:
        return UP.index(ch)
    if ch in LO:
        return 33 + LO.index(ch)
    if ch.isdigit():
        return 90 + int(ch)
    if 'A' <= ch <= 'Z':
        return 100 + ord(ch) - 65
    if 'a' <= ch <= 'z':
        return 126 + ord(ch) - 97
    extra = {'.': 152, ',': 153, '!': 157, '?': 158, "'": 155, '-': 163, ':': 161}
    return extra.get(ch)


def render(lines, scale=4, out='preview_text.png'):
    W = max(sum(1 + widths[char_tile(c)] for c in line if char_tile(c) is not None) for line in lines) + 40
    H = len(lines) * 16 + 20
    canvas = Image.new('RGB', (W * scale, H * scale), (24, 24, 56))
    oy = 10
    for line in lines:
        ox = 10
        for ch in line:
            t = char_tile(ch)
            if t is None:
                continue
            canvas.paste(tile_img(t).resize((TILE * scale, TILE * scale), Image.NEAREST),
                         (ox * scale, oy * scale))
            ox += widths[t] + 1
        oy += 16
    canvas.save(out)


if __name__ == '__main__':
    render(["Всё должно казаться тебе новым...",
            "Просто не мешай мне.",
            "Шёл ёжик, дышал носом, щурился."])
    print('preview_text.png')

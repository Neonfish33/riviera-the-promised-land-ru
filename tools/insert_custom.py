# -*- coding: utf-8 -*-
"""Custom text inserter with deduplication (Atlas doesn't dedup duplicate strings).

Reads an Atlas script (the original in Scripts/), translates via translations.json,
encodes via Insert/IN.tbl, deduplicates identical strings, and writes the text block
and 24-bit pointers directly into the ROM. This avoids the overflow caused by Atlas
writing every duplicate string separately.
"""
import re, io, json, sys, os

def load_tbl(path):
    tbl = {}
    for line in io.open(path, encoding='utf-8'):
        line = line.rstrip('\r\n')
        if '=' not in line:
            continue
        h, g = line.split('=', 1)
        tbl[g] = h.strip().upper()
    return tbl

def encode(s, tbl):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == '<':
            j = s.find('>', i)
            if j == -1:
                break
            code = s[i:j+1]
            if code.startswith('<$'):
                out.append(int(code[2:4], 16))
            else:
                h = tbl.get(code)
                if h:
                    out += bytes.fromhex(h)
                else:
                    raise ValueError(f"unknown control code {code!r}")
            i = j + 1
        else:
            h = tbl.get(c)
            if h:
                out += bytes.fromhex(h)
            else:
                raise ValueError(f"char {c!r} (U+{ord(c):04X}) not in tbl")
            i += 1
    return bytes(out)

def parse_script(path):
    """Return (block_start, block_end, [(ptr_pos, string_content), ...])."""
    text = io.open(path, encoding='utf-8').read()
    jmp = re.search(r'#JMP\(\$([0-9A-Fa-f]+),\$([0-9A-Fa-f]+)\)', text)
    block_start = int(jmp.group(1), 16)
    block_end = int(jmp.group(2), 16)
    lines = text.split('\n')
    pairs = []
    for i, line in enumerate(lines):
        m = re.match(r'#W24\(\$([0-9A-Fa-f]+)\)', line.strip())
        if not m:
            continue
        ptr_pos = int(m.group(1), 16)
        # collect all // lines until <End> (multi-line strings)
        parts = []
        j = i + 1
        while j < len(lines):
            s = lines[j].rstrip('\r')
            if s.startswith('//') and not s.startswith('//POINTER') and not s.startswith('//BLOCK') and not s.startswith('//GAME NAME'):
                parts.append(s[2:])
                if '<End>' in s:
                    break
                j += 1
            elif not s.strip():
                j += 1
                continue
            else:
                break
        if parts:
            pairs.append((ptr_pos, ''.join(parts)))
    return block_start, block_end, pairs

def insert(rom_path, script_path, translations_path, tbl_path, out_path):
    rom = bytearray(open(rom_path, 'rb').read())
    tbl = load_tbl(tbl_path)
    tr = json.load(io.open(translations_path, encoding='utf-8'))
    block_start, block_end, pairs = parse_script(script_path)

    text = bytearray()
    offsets = {}   # encoded bytes -> file offset
    ptr_writes = []  # (ptr_pos, string_offset)
    missing = 0

    for ptr_pos, s in pairs:
        if s in tr:
            s = tr[s]
        else:
            missing += 1
        try:
            enc = encode(s, tbl)
        except ValueError as e:
            print(f"ERROR encoding {s!r}: {e}")
            return False
        if enc in offsets:
            off = offsets[enc]
        else:
            off = block_start + len(text)
            text += enc
            offsets[enc] = off
        ptr_writes.append((ptr_pos, off))

    if block_start + len(text) > block_end + 1:
        print(f"OVERFLOW: text {len(text)} bytes needs up to {block_start+len(text):X}, block ends {block_end:X}")
        print(f"  over by {block_start + len(text) - block_end - 1} bytes")
        return False

    # write text
    rom[block_start:block_start + len(text)] = text
    # write 24-bit little-endian pointers
    for ptr_pos, off in ptr_writes:
        rom[ptr_pos:ptr_pos + 3] = off.to_bytes(3, 'little')

    open(out_path, 'wb').write(rom)
    print(f"{os.path.basename(script_path)}: {len(pairs)} pointers, "
          f"{len(offsets)} unique strings, {len(text)} bytes text "
          f"(budget {block_end - block_start + 1}), {missing} untranslated")
    return True

if __name__ == '__main__':
    insert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

#! /usr/bin/env python3
# Written by Martin v. Löwis <loewis@informatik.hu-berlin.de>

import sys
import os
import struct
import ast

def usage():
    print("Usage: msgfmt.py [options] inputfile", file=sys.stderr)
    print("Options:", file=sys.stderr)
    print("  -o file   output file (default: inputfile.mo)", file=sys.stderr)
    sys.exit(1)

def generate():
    if len(sys.argv) < 2:
        usage()

    infile = sys.argv[-1]
    outfile = None

    if len(sys.argv) >= 4 and sys.argv[1] == '-o':
        outfile = sys.argv[2]

    if outfile is None:
        if infile.endswith('.po'):
            outfile = infile[:-3] + '.mo'
        else:
            outfile = infile + '.mo'

    with open(infile, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    MESSAGES = {}

    msgid = ""
    msgstr = ""
    state = 0 # 0: nothing, 1: msgid, 2: msgstr

    for l in lines:
        l = l.strip()
        if not l or l.startswith('#'):
            continue

        if l.startswith('msgid "'):
            if state == 2:
                MESSAGES[msgid] = msgstr
            msgid = ast.literal_eval(l[6:])
            msgstr = ""
            state = 1
        elif l.startswith('msgstr "'):
            msgstr = ast.literal_eval(l[7:])
            state = 2
        elif l.startswith('"'):
            if state == 1:
                msgid += ast.literal_eval(l)
            elif state == 2:
                msgstr += ast.literal_eval(l)

    if state == 2:
        MESSAGES[msgid] = msgstr

    # Remove empty key if present (header)
    # But actually header is stored with empty string key
    # We need to keep it or handle it.
    # For simple translation, we might not strictly need the header in binary,
    # but gettext usually expects it.

    # Let's write the binary format
    # The format is:
    # magic (0x950412de)
    # revision (0)
    # N (number of strings)
    # O (offset of start of original strings)
    # T (offset of start of translated strings)
    # S (size of hash table, 0 for now)
    # H (offset of hash table)

    keys = sorted(MESSAGES.keys())
    offsets = []
    ids = b''
    strs = b''

    for k in keys:
        v = MESSAGES[k]
        k_enc = k.encode('utf-8')
        v_enc = v.encode('utf-8')

        offsets.append((len(ids), len(k_enc), len(strs), len(v_enc)))
        ids += k_enc + b'\0'
        strs += v_enc + b'\0'

    output_file = open(outfile, 'wb')

    N = len(keys)
    O = 7 * 4 + 4 * 4 # Header size + padding? No.
    # Header is 7 integers: magic, revision, N, O, T, S, H
    # O starts after header + 2 * N * 8 bytes (index tables)

    # Index table for original strings: (length, offset) * N
    # Index table for translated strings: (length, offset) * N

    keystart = 7 * 4 + 8 * N + 8 * N
    valuestart = keystart + len(ids)

    output_file.write(struct.pack('I', 0x950412de)) # Magic
    output_file.write(struct.pack('I', 0)) # Revision
    output_file.write(struct.pack('I', N)) # N
    output_file.write(struct.pack('I', 7 * 4)) # O (start of original index)
    output_file.write(struct.pack('I', 7 * 4 + 8 * N)) # T (start of translated index)
    output_file.write(struct.pack('I', 0)) # S (hash table size)
    output_file.write(struct.pack('I', 0)) # H (hash table offset)

    # Write original index
    for i in range(N):
        l, off, _, _ = offsets[i]
        output_file.write(struct.pack('II', off, keystart + l)) # length, offset
        # Wait, offset is absolute? Yes.
        # My offsets tuple: (id_offset_relative, id_len, str_offset_relative, str_len)
        # keystart is absolute start of ids.

    # Write translated index
    for i in range(N):
        _, _, off, l = offsets[i]
        output_file.write(struct.pack('II', l, valuestart + off))

    output_file.write(ids)
    output_file.write(strs)
    output_file.close()

if __name__ == '__main__':
    generate()

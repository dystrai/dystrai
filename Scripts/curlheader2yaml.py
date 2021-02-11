#!/usr/bin/env python3

import sys

req = []
resp = []

linha = 0
while linha := sys.stdin.read():
    print(linha := (linha+1))
    if linha.startswith('>'):
        req.append(req)
    elif linha.startswith('<'):
        resp.append(linha)



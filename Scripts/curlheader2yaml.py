#!/usr/bin/env python3

import sys
import subprocess

url = input('URL: ')

req = []
resp = []
ps = subprocess.run(['curl', '-v', url], capture_output=True)

reqresp = ps.stderr.splitlines()

for linha in reqresp:
    if linha.startswith('>'):
        req.append(req)
    elif linha.startswith('<'):
        resp.append(linha)



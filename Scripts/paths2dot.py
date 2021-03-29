#!/usr/bin/env python3

from collections import defaultdict
import os
import pathlib
import sys
import typing

if len(sys.argv) < 2:
    print(f'''Uso:
  {sys.argv[0]}
''')
    sys.exit(1)

paths = sys.argv[1:]
gdir = defaultdict(typing.List)

for p in paths:
    path = pathlib.Path(p) # Just to check if it is a valid path.
    dirs = p.split('/')
    if p.startswith('/'):
      dirs[0] = '/'
    for d in dirs[:-1]:
      os.chdir(d)
      inode = os.stat('.')
      print(d)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

caminhos = os.environ['PATH'].split(sep=os.pathsep)

for i,cam in enumerate(caminhos, start=1):
    print(f'{i}. {cam}')


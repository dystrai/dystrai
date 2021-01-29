#! /usr/bin/env python3

import os
import sys

from bs4 import BeautifulSoup
import requests

req = requests.get(sys.argv[1])
html = BeautifulSoup(req.content, 'html.parser')
title = html.head.title.text.strip()

print(f'- [{title}]({req.url})')

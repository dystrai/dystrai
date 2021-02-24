#! /usr/bin/env python3

import os
import sys

from bs4 import BeautifulSoup
import requests

req = requests.get(sys.argv[1])
if 'text/html' in req.headers['Content-type']:
    html = BeautifulSoup(req.content, 'html.parser')
    if html.text.title is None:
        title = html.head.title.text.strip()
    else:
        title = html.find_all('title')[0].contents[0]

    print(f'- [{title}]({req.url})')

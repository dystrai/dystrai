#! /usr/bin/env python3

from datetime import datetime
import os
import sys

from bs4 import BeautifulSoup
import requests
from slugify import slugify

url = sys.argv[1]
now = datetime.now()
today = now.strftime('%F')
req = requests.get(sys.argv[1])
html = BeautifulSoup(req.content, 'html.parser')
title = html.head.title.text.strip()
slug = slugify(title)
fname = f'{today}-{slug}.md'

with open(fname, 'w', encoding='utf-8') as page:
    page.write(f'''# {title}

<{req.url}>
''')

print(f'Link salvo no arquivo: {fname}')

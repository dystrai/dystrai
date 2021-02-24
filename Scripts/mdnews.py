#! /usr/bin/env python3

from datetime import datetime
import getpass
import pwd
import os
import sys

from bs4 import BeautifulSoup
import requests
from slugify import slugify

url = sys.argv[1]
now = datetime.now()
today = now.strftime('%F')
data = now.strftime('%d/%m/%Y')
hora = now.strftime('%T')
usuario = getpass.getuser()
try:
    autor = pwd.getpwnam(usuario).pw_gecos.split(',')[0]
except:
    autor = usuario.title()

req = requests.get(sys.argv[1])
if 'text/html' in req.headers['Content-type']:
    html = BeautifulSoup(req.content, 'html.parser')
    if html.text.title is None:
        title = html.head.title.text.strip()
    else:
        title = html.find_all('title')[0].contents[0]

    slug = slugify(title)
    fname = f'{today}-{slug}.md'

    with open(fname, 'w', encoding='utf-8') as page:
        page.write(f'''# {title}

- Autor: {autor}
- Última atualização: {data} à(s) {hora}

\\<<{req.url}>\\>
''')

    print(f'Link salvo no arquivo: {fname}')

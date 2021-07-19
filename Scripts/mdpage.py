#!/usr/bin/env python3
'''
Save Markdown page with title and link for an URL
'''
import os
import sys

from bs4 import BeautifulSoup
import requests
from slugify import slugify

def save_page_link(url: str):
    req = requests.get(url)
    if 'text/html' in req.headers['Content-type']:
        html = BeautifulSoup(req.content, 'html.parser')
        if html.text.title is None:
            title = html.head.title.text.strip()
        else:
            title = html.find_all('title')[0].contents[0]

        slug = slugify(title)
        fname = f'{slug}.md'

        with open(fname, 'w', encoding='utf-8') as page:
            page.write(f'''# {title}

\<<{req.url}>\>
''')

        print(f'Link salvo no arquivo: {fname}')

def main():
    if len(sys.argv) > 1:
        for url in sys.argv[1:]:
            save_page_link(url)
    else:
        try:
            while (url := input('URL: ')):
                save_page_link(url)
        except EOFError as erro:
            pass        


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
'''
Save Markdown page with title and link for an URL
'''

from argparse import ArgumentParser
from getpass import getuser
import os
import sys
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
import requests
from slugify import slugify

global usuario
usuario = getuser()

# Based on: https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
def uri_validator(url: str) -> bool:

    try:
        resultado = urlparse(url)
        return all([resultado.scheme, resultado.netloc])
    except:
        return False

def emb_youtube_video(v: str):

    return f'''\
<iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/{v}" 
        title="YouTube video player" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
        >
</iframe>    
'''


def save_page_link(url: str, guardar_usuario: bool):
    req = requests.get(url)
    url_analisada = urlparse(url)

    if req.ok and 'text/html' in req.headers['Content-type']:
        html = BeautifulSoup(req.content, 'html.parser')
        if html.text.title is None:
            title = html.head.title.text.strip()
        else:
            title = html.find_all('title')[0].contents[0]

        slug_title = slugify(title)
        if guardar_usuario:
            slug_user = slugify(usuario)
            fname = f'{slug_user}_{slug_title}.md'
        else:
            fname = f'{slug_title}.md'

        with open(fname, 'w', encoding='utf-8') as page:
            page.write(f'''# {title}

\<<{req.url}>\>
''')
            if url_analisada.hostname == 'www.youtube.com':
                qs_analisada = parse_qs(url_analisada.query)
                if 'v' in qs_analisada:
                    page.write(f'\n\n{emb_youtube_video({qs_analisada["v"][0]})}\n')

            page.write('''\n\n## Anotações

''')

        print(f'Link salvo no arquivo: {fname}')

def main():

    analisador_args = ArgumentParser()
    analisador_args.add_argument('-u', '--usuario', help='Insere nome do usuário no início do nome do arquivo', action="store_true")
    analisador_args.add_argument('url', nargs='*', help='URL a ser analisada')

    # DEBUG
    global args
    args = analisador_args.parse_args()

    if len(args.url) > 0:
        for url in args.url:
            save_page_link(url, guardar_usuario=args.usuario)
    else:
        try:
            while (url := input('URL: ')):
                save_page_link(url, guardar_usuario=args.usuario)
        except EOFError as erro:
            pass        
        except KeyboardInterrupt as erro:
            pass
        except:
            pass

if __name__ == '__main__':
    main()

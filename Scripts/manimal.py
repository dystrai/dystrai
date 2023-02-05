#!/usr/bin/env python3

import argparse
import pathlib
import pwd
import os
import sys

from bs4 import BeautifulSoup
import requests
from slugify import slugify

MANIMAL_LIB = '/var/lib/manimal'
manimal_dir = pathlib.Path(MANIMAL_LIB)

def main():
    disciplina = os.getenv('DISCIPLINA')
    if not disciplina:
        print('Por gentileza, especifique para qual disciplina que você deseja o animal.')
        print('Defina e exporte a variável de ambiente DISCIPLINA')

        shell = os.getenv('SHELL')
        if shell.endswith('zsh'):
            print('No zsh, isto é feito editando-se o arquivo "~/.zshenv"')
        elif shell.endswith('bash'):
            print('No bash, isto é feito editando-se o arquivo "~/.bashrc')
        else:
            print('Consulte seu shell para descobrir como definir a variável de ambiente.')
        sys.exit(1)

    else:
        disc_dir = manimal_dir / disciplina
        if disc_dir.exists() and disc_dir.is_dir():
            parser = argparse.ArgumentParser()
            parser.add_argument('animal', help='Nome do animal que você deseja representar')
            parser.add_argument('url', help='URL do artigo da Wikipedia sobre o animal escolhido')
            args = parser.parse_args()

            global animal_file
            animal_dir = disc_dir / 'animal'
            animal_file = animal_dir / args.animal

            if not animal_file.exists():
                if not args.url.startswith('https://pt.wikipedia.org'):
                    print('Sinto muito, mas por enquanto, só aceitamos artigos em português.')
                    sys.exit(1)
                resp = requests.get(args.url)
                if resp.ok:
                    html_parser = BeautifulSoup(resp.text, 'html.parser')
                    if html_parser.find(href="/wiki/Animalia"): # Just a guess
                        animal_file.touch()
                        with animal_file.open(encoding='utf-8', mode='w') as arquivo:
                            arquivo.write(args.url)
            else:   # Who does it belong to?
                af_stat = animal_file.stat()
                if af_stat.st_uid == os.getuid():
                    print(f'Você já escolheu {args.animal} para {disciplina}.')
                else:
                    dados_prop = pwd.getpwuid(af_stat.st_uid)
                    nome_prop = dados_prop.pw_gecos.split(',')[0]
                    dados_usuario = pwd.getpwuid(os.getuid())
                    nome_usuario = dados_usuario.pw_gecos.split(',')[0]
                    prim_nome_usuario = nome_usuario.split()[0]
                    print(f'{prim_nome_usuario.title()}, por gentileza, escolha outro animal.')
                    print(f'O animal {args.animal} já foi escolhido por {nome_prop}.')




        else:
            print(f'O diretório da disciplina "{disciplina}" não existe.')
            print('Peça para seu professor criá-la ou certifique-se que o nome da disciplina está correto.')
            sys.exit(2)

if __name__ == '__main__':
    main()

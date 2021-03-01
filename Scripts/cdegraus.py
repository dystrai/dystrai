#!/usr/bin/env python3

import argparse
import getpass
import os.path
import pathlib
import pwd
import sys
import subprocess
from typing import List

usuario = getpass.getuser()
nome = pwd.getpwnam(usuario).pw_gecos
if nome:
    if ',' in nome:
        nome = nome.split(',')[0]
    if ' ' in nome:
        nome = nome.split(' ')[0]
else:
    nome = usuario

def cdegraus(caminho: pathlib.Path, verboso: bool, permissoes: bool): #-> List[str]:
    if caminho.is_dir():
        degraus = str(caminho).split('/')
        if caminho.is_absolute():
            degraus[0] = ('/')
        print(f'{nome}, aqui estão os passos para chegar até <{caminho}>:')
        if verboso:
            for i,d in enumerate(degraus, start=1):
                print(f'{3*i}. cd {d}')
                print(f'{3*i+1}. pwd')
                print(f'{3*i+1}. ls -F1')
        elif permissoes:
            for i,d in enumerate(degraus, start=1):
                print(f'{2*i}. ls -ld {d}')
                print(f'{2*i+1}. cd {d}')
        else:
            for i,d in enumerate(degraus, start=1):
                print(f'{i}. cd {d}')            
    elif caminho.is_file():
        print(f'{caminho} é um arquivo.')
        print(f'Experimente: {sys.argv[0]} {os.path.dirname(caminho)}')

def main():
    interpretador = argparse.ArgumentParser()
    interpretador.add_argument('caminho', help='O caminho para um diretório do sistema.')
    interpretador.add_argument('-p', '--permissoes', action="store_true", help='Lista as permissões de cada diretório.')
    interpretador.add_argument('-v', '--verboso', action="store_true", help='Se certifica dos diretórios que está entrando.')
    args = interpretador.parse_args()
    cam = pathlib.Path(args.caminho)
    cdegraus(cam, args.verboso, args.permissoes)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3

import argparse
from copy import copy
import getpass
import os
import pathlib
import pwd
import sys


usuario = getpass.getuser()
nome = pwd.getpwnam(usuario).pw_gecos
if nome:
    if ',' in nome:
        nome = nome.split(',')[0]
    if ' ' in nome:
        nome = nome.split(' ')[0]
else:
    nome = usuario

def cdegraus(caminho: pathlib.Path):
    if caminho.is_dir():
        copia = copy(caminho)
        degraus = str(caminho).split('/')
        if caminho.is_absolute():
            degraus[0] = ('/')
        print(f'{nome}, aqui estão os passos para chegar até <{caminho}>:')
        print()

        for i,d in enumerate(degraus, start=1):
            print(f'-> [{os.getcwd()}]')
            os.chdir(d)
            print(f'{i}. cd {d}')

        print(f'-> [{os.getcwd()}]')
        


    elif caminho.is_file():
        print(f'{caminho} é um arquivo.')
        print(f'Experimente: {sys.argv[0]} {os.path.dirname(caminho)}')

def main():
    interpretador = argparse.ArgumentParser()
    interpretador.add_argument('caminho', help='O caminho para um diretório do sistema.')
    args = interpretador.parse_args()
    cam = pathlib.Path(args.caminho)
    cdegraus(cam)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3

from collections import defaultdict
from getpass import getuser
from os import makedirs, stat, getpid
from os.path import sep, isfile, exists
from pprint import pprint
import sys

from graphviz import Digraph

caminhos = sys.argv[1:]
if len(caminhos) == 0:
    sys.stderr.write(f'Uso: {sys.argv[0]} [CAMINHO]...\n')
    sys.exit(1)

try:
    assert all([exists(c) for c in caminhos])
except AssertionError as erro:
    sys.stderr.write(f'{erro}\n')
    sys.stderr.write('Todos os caminhos devem ser válidos.')

class Link:
    def __init__(self, para: str, nome: str):
        self.para = para
        self.nome = nome

grafo = {}

for path in caminhos:
    degraus = path.split(sep)
    if 0 == len(degraus[0]):
        degraus[0] = sep  # Raiz do sistema de arquivos

    i = 0
    d = degraus[0]
    cam_parcial = d
    dados = stat(cam_parcial)
    inode = str(dados.st_ino)
    inodes = [inode]

    for i,nome in enumerate(degraus[1:], start=1):
        cam_abs = degraus[0]+'/'+'/'.join(degraus[1:i+1])
        dados = stat(cam_abs)
        inode = str(dados.st_ino)
        inodes.append(inode)
        grafo[(inodes[i-1], nome)] = (inodes[i], isfile(cam_abs))


dot = Digraph('Caminho dos inodes', format='png')
dot.attr('graph', rankdir='LR')

for (orig,nome),(dest, eh_arquivo) in grafo.items():
    if eh_arquivo:
        dot.attr('node', shape='ellipse')
    else:
        dot.attr('node', shape='rectangle')

    dot.edge(orig, dest, nome)

USR = getuser()
PID = getpid()
DCR = f'/var/www/html/sd20202/{USR}'
PNG = f'{DCR}/{PID}'
URL = f'https://turmas.oulu.ifrn.edu.br/sd20202/{USR}/{PID}.png'
makedirs(DCR, mode=0o755, exist_ok=True)
dot.render(PNG, view=False)
print('Grafo gerado e salvo em:')
print(f'  {URL}')


#!/usr/bin/env python3

import os
import sys
from pathlib import Path

from graphviz import Digraph
from slugify import slugify

BARRA = 'barra'

grafo = Digraph('Árvore de diretórios', format='png', strict=True)
grafo.attr('graph', rankdir='LR')
# grafo.attr('graph', splines='false') # straight lines

def atualizar_grafo(caminho: Path):
    partes = caminho.parts
    partes_formatadas = [slugify(p).replace('-', '_') for p in caminho.resolve().parts]
    partes_formatadas[0] = BARRA
    grafo.node(name=BARRA, label=partes[0], shape='folder')
    nomes = [BARRA]

    for i,p in enumerate(partes_formatadas[1:], start=1):
        fspath = Path(os.sep + os.sep.join(partes[1:i+1]))
        nome = '_'.join(partes_formatadas[:i+1])
        nomes.append(nome)

        if fspath.is_dir():
            forma = 'folder'
        else:
            forma = 'plain'

        grafo.node(name=nome, label=partes[i], shape=forma)
        grafo.edge(nomes[i-1], nome)


def main():
    if len(sys.argv) < 2:
        print(f'''\
Uso:
  {sys.argv[0]} CAMINHO [CAMINHO...]
''')
        sys.exit(1)

    for caminho in sys.argv[1:]:
        atualizar_grafo(Path(caminho))

    grafo.view()
    grafo.render('/tmp/arvore')

if __name__ == '__main__':
  main()

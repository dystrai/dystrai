#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import shutil

from graphviz import Digraph
from slugify import slugify

BARRA = 'barra'

def atualizar_grafo(grafo: Digraph, caminho: Path):
    partes = caminho.parts
    partes_formatadas = [slugify(p).replace('-', '_') for p in caminho.parts]
    partes_formatadas[0] = BARRA
    grafo.node(name=BARRA, label=partes[0], shape='folder')
    nomes = [BARRA]

    for i,p in enumerate(partes_formatadas[1:], start=1):
        print(i, p)
        fspath = Path(os.sep + os.sep.join(partes[1:i+1]))
        nome = '_'.join(partes_formatadas[:i+1])
        nomes.append(nome)

        if fspath.is_dir():
            forma = 'folder'
        else:
            forma = 'plain'

        print(nome, i, partes)
        grafo.node(name=nome, label=partes[i], shape=forma)
        grafo.edge(nomes[i-1], nome)


def main():
    if len(sys.argv) < 4:
        print(f'''\
Uso:
  {sys.argv[0]} CAMINHO [CAMINHO...]
''')
        sys.exit(1)

    gname = sys.argv[1]
    grafo = Digraph(sys.argv[1], format='png', strict=True)
    grafo.attr('graph', rankdir='LR')
    # https://stackoverflow.com/questions/6450765/how-do-you-center-a-title-for-a-diagram-output-to-svg-using-dot
    grafo.attr('graph', label=sys.argv[2])
    grafo.attr('graph', labelloc='t')
    # grafo.attr('graph', splines='false') # linhas retas (straight lines)

    for caminho in sys.argv[2:]:
        atualizar_grafo(grafo, Path(caminho))

    grafo.view()
    grafo.render()
    shutil.move(f'{gname}.gv.png', f'{gname}.png')

if __name__ == '__main__':
  main()

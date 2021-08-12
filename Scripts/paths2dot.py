#!/usr/bin/env python3

from collections import defaultdict
import os
import pathlib
import sys

import graphviz

BARRA = '/'


arvore_inodes = defaultdict(set)
nome_para_inode = {}

def atualizar_arvore(path: str):

  caminho = pathlib.Path(path)

  if caminho.exists() and caminho.is_dir():
      cam_abs = str(caminho.resolve(True))
      degraus = cam_abs.split(BARRA)
      degraus[0] = BARRA

      dir_pai = pathlib.Path(degraus[0])
      inode_pai = os.stat(str(dir_pai)).st_ino
      nome_para_inode[inode_pai] = degraus[0]

      for i,p in enumerate(degraus[1:]):
          dir_filho = dir_pai / p
          inode_filho = os.stat(str(dir_filho)).st_ino
          nome_para_inode[inode_filho] = p
          arvore_inodes[inode_pai].add(inode_filho)

          dir_pai = dir_filho
          inode_pai = inode_filho


def main():
    if len(sys.argv) < 2:
        print(f'''\
Uso:
  {sys.argv[0]} CAMINHO [CAMINHO...]
''')
        sys.exit(1)

    for caminho in sys.argv[1:]:
        atualizar_arvore(caminho)

if __name__ == '__main__':
  main()
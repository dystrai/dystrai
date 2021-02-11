#!/usr/bin/env python3

from dataclasses import dataclass

# Criar uma árvore com os caminhos e só posteriormente gerar o graphviz

@dataclass
class Arquivo:
  nome: str

class Diretorio:
  def __init__(self, nome: str):
    super().__init__()
    self._nome = nome
    self.conteudo = {}

  @property
  def nome(self):
    return self._nome


import pathlib
import sys

if len(sys.argv) < 2:
    print(f'''Uso:
  {sys.argv[0]}
''')
    sys.exit(1)

paths = sys.argv[1:]
gvpaths = []

for p in paths:
    path = pathlib.Path(p) # Just to check if it is a valid path.
    dirs = p.split('/')

    # Trim
    if '' == dirs[0]: del dirs[0]
    if '' == dirs[-1]: del dirs[-1]

    # Insert '/' at the beginning
    dirs.insert(0, '/')

    quoted_dirs = [f'"{d}"' for d in dirs]
    gvpaths.append('  ' + ' -> '.join(quoted_dirs) + ';')

body = '\n'.join(gvpaths)
print(f'''digraph path {{
  rankdir=LR;    
{body}
}}''')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


if len(sys.argv) != 2:
    print('Uso: onde-estah COMANDO')
    sys.exit(2)
else:
    comando = sys.argv[1]
    caminhos = os.environ['PATH'].split(sep=os.pathsep)

    for cam in caminhos:
        cam_completo = os.path.join(cam, comando)
        if os.path.exists(cam_completo):
            print(f'O comando "{comando}" foi achado no diretório "{cam}"')
            sys.exit(0)
        
print(f'O comando "{comando}" não foi achado em nenhum dos caminhos de busca de comandos.')
sys.exit(1)


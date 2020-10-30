#!/usr/bin/env python3

import subprocess
import sys

import googletrans

if len(sys.argv) > 1:
    comando = ' '.join(sys.argv[1:])
    saida = subprocess.getoutput(comando)
    tradutor = googletrans.Translator()
    for linha in saida.splitlines():
        print(tradutor.translate(linha, src='en', dest='pt').text)
else:
    sys.exit(1)

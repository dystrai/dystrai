#!/usr/bin/env python3

from collections import defaultdict
import os
import sys


if len(sys.argv) != 2:
    print(f'Uso: {sys.argv[0]} ARQUIVO', file=sys.stdout)
    sys.exit(1)

texto = open(sys.argv[1], 'r', encoding='utf-8').read()
linhas = texto.splitlines()

# Associa números a capítulos
num_cap = {}

ini_cap = {}
for i,l in enumerate(linhas):
    if l.startswith('CAPÍTULO'):
        _,cap = l.split()
        i_cap = len(num_cap)
        num_cap[i_cap] = cap
        ini_cap[i_cap] = i

tit_cap = {cap:linhas[i+1] for cap,i in ini_cap.items()}
QT_CAPS = len(num_cap)

fim_cap = {c:ini_cap[c+1]-1 for c in range(QT_CAPS-1)}
fim_cap[QT_CAPS-1] = -1

ini_art = {}
fim_art = {}
arts_cap = defaultdict(list)

for cap in range(QT_CAPS):
    ini = ini_cap[cap]
    fim = fim_cap[cap]
    for i,l in enumerate(linhas[ini:fim], start=ini):
        if l.startswith('Art.'):
            _,art,_ = l.split(maxsplit=2)
            art = int(art.replace('º', '').replace('.', ''))
            ini_art[art] = i
            arts_cap[cap].append(art)
    for art in arts_cap[cap][:-1]:
        fim_art[art] = ini_art[art+1]
    fim_art[arts_cap[cap][-1]] = fim_cap[cap]

os.makedirs('docs', exist_ok=True)

QT_ARTS = len(ini_art)
artigos = {}
for art in range(1, QT_ARTS+1):
    ini = ini_art[art]
    fim = fim_art[art]
    conteudo = '\n'.join(linhas[ini:fim])
    artigos[art] = conteudo
    with open(os.path.join('docs', f'art-{art}.md'), mode='w', encoding='utf-8') as arq_art:
        arq_art.write(f'''\
# Artigo {art}

{conteudo}
''')

for cap in range(QT_CAPS):
    with open(os.path.join('docs', f'capitulo-{cap+1}.md'), mode='w', encoding='utf-8') as arq_cap:
        arq_cap.write(f'''\
# Capítulo {num_cap[cap]} -- {linhas[ini_cap[cap]+1].lower().capitalize()}

''')
        for art in arts_cap[cap]:
            arq_cap.write(f'- [Artigo {art}](art-{art}.md)\n')
        


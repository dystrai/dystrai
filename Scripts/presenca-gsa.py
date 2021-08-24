#!/usr/bin/python3

"""Lista de presença a partir dos bate papos do Google Sala de Aula
"""


from glob import glob
import re

bate_papos = glob('*.sbv')

for nome_arq in bate_papos:
    casamento = re.match(r'.*\((?P<ano>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2})', nome_arq)
    print('=== Lista de presença do dia {dia}/{mes}/{ano} ==='.format(**casamento.groupdict()))
    print(f'    [{nome_arq}]')
    print()
    with open(nome_arq) as arq:
        presentes = set()
        conteudo = arq.read()
        conversas = conteudo.split('\n\n')
        if not conversas[-1]: del conversas[-1]
        for c in conversas:
            autor = c.splitlines()[1].split(':', maxsplit=1)[0]
            presentes.add(autor)
    
        print('-', '\n- '.join(sorted(presentes)))
        
    input('\nPressione <ENTER> para exibir a próxima lista.')
    

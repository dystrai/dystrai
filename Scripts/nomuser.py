#!/usr/bin/env python3

'''
Sugere nome de usuário.
'''

import sys

PREPS_DE_NOMES = ('de', 'da', 'das', 'do', 'dos', 'e')

def nomuser(nome_completo: str) -> str:
    nome_sobrenomes = [n.lower() for n in nome_completo.split() if n.lower() not in PREPS_DE_NOMES]
    if len(nome_sobrenomes) > 1:
        # Retorna {{nome}}.{{último sobrenome}}
        return f'{nome_sobrenomes[0]}.{nome_sobrenomes[-1]}'
    else:
        return nome_completo.lower()

def main():

    # How to receive arguments via shell pipe in python?
    # https://stackoverflow.com/questions/6106437/how-to-receive-arguments-via-shell-pipe-in-python
    iterador = sys.argv[1:] if len(sys.argv) > 1 else sys.stdin

    for nome in iterador:
        print(nomuser(nome))


if __name__ == '__main__':
    main()

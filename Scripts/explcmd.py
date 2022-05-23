#!/usr/bin/env python3

"""
explicacmd: Explica comando com Markdown
"""

import sys

class Argumento:
    def __init__(self, arg: str, num: int) -> None:
        self.arg = arg if " " not in arg else f"'{arg}'"
        self.num = num
        if len(arg) == 1:
            self.ornamento = '|'
        elif not " " in arg:
            self.ornamento = f'\\{"_"*(len(arg)-2)}/'
        else:
            self.ornamento = f'\\{"_"*(len(arg))}/'
        self.num_centralizado = str(self.num).center(len(self.ornamento), ' ')

    def __str__(self) -> str:
        return self.arg

def main():
    
    if len(sys.argv) > 1:
        args = [Argumento(arg, i) for i,arg in enumerate(sys.argv[1:], start=1)]
        print('```')
        print(' '.join([a.arg for a in args]))
        print(' '.join([a.ornamento for a in args]))
        print(' '.join([str(a.num).center(len(a.ornamento), ' ') for a in args]))
        print('```')
        print()
        for a in args:
            print(f'{a.num}. `{a.arg}`')
            print()
            print(f'{" "*(len(str(a.num))+2)} Explicação')
            print()

    else: # Ler da entrada padrão
        while linha := sys.stdin.readline():
	        quebrada = linha.split()
        # TODO: The same as above, but taking into account the number shown at the beginning of line (history number?)
if __name__ == '__main__':
    main()



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

    def __str__(self) -> str:
        return self.arg
        
args = [Argumento(arg, i) for i,arg in enumerate(sys.argv[1:], start=1)]
print('```')
print(' '.join([a.arg for a in args]))
print(' '.join([a.ornamento for a in args]))
print(' '.join([str(a.num).center(len(a.ornamento), ' ') for a in args]))
print('```')
print()
for a in args:
    print(f'{a.num}. `{a.arg}`')
    print(f'{" "*(len(str(a.num))+2)} Explicação')
    print()





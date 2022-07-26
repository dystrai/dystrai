#!/usr/bin/env python3

"""
explicacmd: Explica comando com Markdown
"""

from pathlib import Path
import sys

try:
    from slugify import slugify
except:
    print('Por favor, instale o módulo slugify!')
    print('Execute: pip3 install python-slugify')
    sys.exit(1)

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
        if ' ' in self.arg:
            return f'"{self.arg}"'
        else:
            return self.arg

def main():
    
    if len(sys.argv) > 1:
        slug = slugify(' '.join(sys.argv[1:]))
        args = [Argumento(arg, i) for i,arg in enumerate(sys.argv[1:], start=1)]

        cam_arq_saida = Path() / 'saidas' / f'{slug}.txt'
        with cam_arq_saida.open(mode='w', encoding='utf-8') as arq_saida:
            pass

        with open(f'{slug}.md', mode='w', encoding='utf-8') as arquivo_expl:
            arquivo_expl.write(f'''\

(comando:{slug})=

# Comando `{' '.join([str(a) for a in args])}`


''')            
            arquivo_expl.write('```'+'\n')
            arquivo_expl.write(' '.join([a.arg for a in args])+'\n')
            arquivo_expl.write(' '.join([a.ornamento for a in args])+'\n')
            arquivo_expl.write(' '.join([str(a.num).center(len(a.ornamento), ' ') for a in args])+'\n')
            arquivo_expl.write('```'+'\n')
            arquivo_expl.write('\n')
            for a in args:
                arquivo_expl.write(f'{a.num}. `{a.arg}`'+'\n')
                arquivo_expl.write('\n')
                arquivo_expl.write(f'{" "*(len(str(a.num))+2)} Explicação'+'\n')
                arquivo_expl.write('\n')

            arquivo_expl.write(f'''

## Saída

```{{literalinclude}} saidas/{slug}.txt
:linenos:
```
''')


    
if __name__ == '__main__':
    main()



#!/usr/bin/env python3

import pathlib
import subprocess
import sys

# Document commands' help
# TODO: Check if a command is built-in or external

# Documenta a ajuda de comandos.
# A FAZER: Verificar se o comando é interno ou externo ao shell
#
# * Interno do bash: `help COMANDO`
# * Interno do zsh: `run-help COMANDO`
# * Externo: `COMANDO --help`


if len(sys.argv) < 2:
    print(f'''\
Usage:
  {sys.argv[0]} COMMAND...
''')
    sys.exit(1)

for cmd in sys.argv[1:]:
    fname = pathlib.Path(f'{cmd}.md')
    if fname.exists():
        print("Arquivo de ajuda já encontrado para comando {cmd}: <{cmd}.md>.")
        continue
    else:
        cmdhelp = subprocess.run(['{cmd}', '--help'], capture_output=True)
        with fname.open('w', encoding='utf-8') as fobj:
            fobj.write('''\
({cmd})=

# {cmd}

```
{fobj.stdout}
```
'''
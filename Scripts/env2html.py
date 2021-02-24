#!/usr/bin/env python3

from os import environ
import markdown


def env2md():
    rows = []
    for var in sorted(environ.keys()):
        rows.append(f'| {var} | {environ[var]} |')

    return '\n'.join(rows)

print("Content-type: text/html;charset=utf-8")
print()

pg_header = "# Variáveis de ambiente"

tb_header = '''
| Variável | Valor |
| -------- | ----- |
'''

tb_body = env2md()

md = f'''
{pg_header}

{tb_header}

{tb_body}
'''

print(md)
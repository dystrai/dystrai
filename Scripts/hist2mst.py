#! /usr/bin/env python3

import sys

comandos = '''hostname
whoami
ln -sv /var/www/html/  www
ls
ls -l www
ls
cd www
ls
mkdir -v jurandy
cd jurandy/
ls
micro pagina.md
pandoc -o pagina.docx pagina.md
pandoc -o pagina.html pagina.md
micro pagina.md
pandoc -o pagina.html pagina.md
history'''.splitlines()

# for i,linha in enumerate(comandos, start=1):
# 	cmd,args = linha.split(maxsplit=1) if ' ' in linha else (linha,'')
# 	print(f'{i}. {{ref}}`help-{cmd}` {args}')
# 	with open(f'{cmd}.md', 'w', encoding='utf-8') as arq:
# 		arq.write(f'''(help-{cmd})=

# # {cmd}

# ''')

while linha := sys.stdin.readline():
	quebrada = linha.split()
	i,cmd = quebrada[:2]
	args = quebrada[2:]
	print(f'{i}. {{ref}}`help-{cmd}` {" ".join(args)}')
	try:
		with open(f'/tmp/{cmd}.md', 'w', encoding='utf-8') as arq:
			arq.write(f'''(help-{cmd})=

# {cmd}

''')
	except:
		pass


#!/usr/bin/env python3

# Texto copiado do Google Meet
batepapo = '''\
{nome completo}
{marca de tempo}
{mensagem}
{linha em branco}
'''

linhas_bp: list[str] = batepapo.splitlines()

nomes = [linhas_bp[4*n] for n in range(len(linhas_bp)//4)]

presentes = sorted(set(nomes))

for i, estudante in enumerate(presentes, start=1):
    print(f"{i}. {estudante.title()}")

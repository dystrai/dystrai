# -*- coding: utf-8 -*-
"""
Cria um diretório por estudante
"""

import os
import sys

with open(sys.argv[1]) as arq:
    nomes = arq.read().splitlines()

    nomes_sobrenomes = []
    for n in nomes:
        nome_quebrado = n.split()
        if len(nome_quebrado[1]) > 3:
            ns = '-'.join(nome_quebrado[:2])
        else:
            nome_quebrado[1] = nome_quebrado[1].lower()
            ns = '-'.join(nome_quebrado[:3])
        
        nomes_sobrenomes.append(ns)
        
    for ns in nomes_sobrenomes:
        os.makedirs(ns, exist_ok=True)


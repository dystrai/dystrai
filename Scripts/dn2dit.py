#! /usr/bin/env python3

'''
Convert LDAP DNs to DIT
'''

from collections import defaultdict
import sys

def exibe(rdn, nivel):
    print(f'{3*nivel*" "}{rdn}')
    for ent in entradas[rdn]:
        exibe(ent, nivel+1)

entradas = defaultdict(list)
dcs = set()

for dn in sys.stdin:
    rdns = list(reversed(dn.split(',', maxsplit=dn.count(',')-1)))
    rdns[0] = rdns[0].strip()
    dcs.add(rdns[0])
    for i,atual in enumerate(rdns[:-1]):
        prox = rdns[i+1]
        if not prox in entradas[atual]:
            entradas[atual].append(prox)

for dc in list(sorted(dcs)):
    exibe(dc, 0)

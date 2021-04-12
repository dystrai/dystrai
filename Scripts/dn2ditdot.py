#! /usr/bin/env python3

'''
Convert LDAP DNs to DIT
'''

from collections import defaultdict
import sys

from graphviz import Digraph

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

def arestas(rdn, dot):
    for ent in entradas[rdn]:
        dot.edge(rdn, ent)
        arestas(ent, dot)

dcs = list(sorted(dcs))

dot = Digraph('DIT', format='png')
dot.attr('graph', rankdir='LR')
dot.attr('node', shape='rectangle')

for dc in dcs:
    arestas(dc, dot)

PNG = '/tmp/dit.dot'
dot.render(PNG, view=False)
    
    

#!/usr/bin/env python3

import cgi, cgitb
from bs4 import BeautifulSoup

print("Content-type: text/html")
print()

formulario = cgi.FieldStorage()

matricula = formulario.getvalue('matricula')
usuario = formulario.getvalue('usuario')
url = formulario.getvalue('url')

conteudo = open('/home/ubuntu/index.html', 'r').read()

if matricula and usuario and url:
    sopa = BeautifulSoup(conteudo)
    matf = sopa.find('input', {'id': 'matricula'})
    usuf = sopa.find('input', {'id': 'usuario'})
    url = sopa.find('input', {'id': 'url'})
    matf['value'] = matricula
    usuf['value'] = usuario
    url['value'] = usuario
    print(sopa)
else:
    print(conteudo)

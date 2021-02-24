#!/usr/bin/env python3

from datetime import datetime
from os import environ
import pathlib

agora = datetime.now()
ano_mes_dia = datetime.strftime(agora, '%F')

if uri := environ.get('REQUEST_URI'):
    uri_quebrada = uri.split('/')
    if len(uri_quebrada) == 3:
        _,_,disciplina = uri_quebrada
        nova_uri = f'/roteiro/{disciplina}/{disciplina}-{ano_mes_dia}.sh'
        caminho = pathlib.Path(f"{environ['DOCUMENT_ROOT']}{nova_uri}")
        print(caminho)
        if not caminho.exists():
            nova_uri = "/hoje/aviso?disciplina=asa"
    #nova_localizacao = f"{environ['REQUEST_SCHEME']}://{environ['HTTP_HOST']}:{environ['SERVER_PORT']}{nova_uri}"

print("Content-type: text/plain;charset=utf-8")
#print("Status: 303 See other")
#print("Location: ")
print()
print(nova_uri)

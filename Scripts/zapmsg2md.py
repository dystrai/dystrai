#!/usr/bin/env python3
# -*- coding: utf-8 -*-
    
"""Converte mensagens de WhatsApp para Markdown."""

from argparse import ArgumentParser
import re

parser = ArgumentParser(description='Converte mensagens de WhatsApp para Markdown.')
parser.add_argument('arquivo', help='Arquivo de texto com mensagens de WhatsApp.')
args = parser.parse_args()

if args.arquivo.endswith('.txt'):
    arquivo_saida = args.arquivo.replace('.txt', '.md')
    regex = re.compile(r'^(\d+\/\d+\/\d+ \d+:\d+ - )(.+)')

    with open(args.arquivo) as conversa, \
        open(arquivo_saida, 'w') as conversa_formatada:

        texto: list[str] = conversa.read().splitlines()

        for linha in texto:
            if match := regex.match(linha):
                marco_temporal,mensagem = linha.split('-', maxsplit=1)
                conversa_formatada.write(f'- {marco_temporal} - {mensagem}\n')
            else:
                conversa_formatada.write(f'  {linha}\n')

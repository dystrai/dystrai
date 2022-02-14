#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Cria contas locais de usuários Linux a partir dos dados vindos de um arquivos CSV
'''

__author__ = "Jurandy Soares"
__date__ = "14 February 2022"

import argparse
from collections import namedtuple
import csv
import os
import pathlib

analisador = argparse.ArgumentParser()
analisador.add_argument('arquivo_csv')
args = analisador.parse_args()

nome_arq = args.arquivo_csv
caminho_arq = pathlib.Path(nome_arq)



if caminho_arq.exists() and caminho_arq.is_file():

    leitor = csv.DictReader(caminho_arq.open('r', encoding='utf-8'))
    assert {'Nome', 'Matricula', 'Usuario'}.issubset(set(leitor.fieldnames))
    Aluno = namedtuple('Usuario', leitor.fieldnames)

    for dados_aluno in leitor:
        aluno = Aluno(**dados_aluno)
        cmd_cria_usr = f'useradd -m -c "{aluno.Nome},{aluno.Matricula}" -s /bin/bash {aluno.Usuario}'
        cmd_def_senha = f'echo {aluno.Usuario}:{aluno.Matricula} | chpasswd'

        assert os.geteuid() == 0
        os.system(cmd_cria_usr)
        os.system(cmd_def_senha)

 



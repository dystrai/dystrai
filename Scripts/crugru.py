#!/usr/bin/env python3
"""crugru: Cria usuários e grupos
"""
import argparse
import csv
from dataclasses import dataclass
import pathlib
import shlex
import subprocess
import sys

@dataclass
class Estudante:
    usuario: str
    matricula: str
    nome: str
    email: str

def main():
    analisador: argparse.ArgumentParser = argparse.ArgumentParser('crug')
    analisador.add_argument('csv', help='Arquivo CSV com campos ["Usuário", "Matrícula", "Nome", "E-mail escolar"]')
    argumentos: argparse.Namespace = analisador.parse_args()

    caminho_csv: pathlib.Path = pathlib.Path(argumentos.csv)
    if caminho_csv.exists() and caminho_csv.is_file():
        leitor = csv.DictReader(caminho_csv.open(mode='r', encoding='utf-8'))
        estudantes = {}

        for linha in leitor:
            estudante = Estudante(linha['Usuário'], linha['Matrícula'], linha['Nome'], linha['E-mail escolar'])
            estudantes[estudante.usuario] = estudante
            cmd1 = f"useradd -m -s /bin/zsh -c '{estudante.nome}' {estudante.usuario}"
            cmd1_args = shlex.split(cmd1)
            subprocess.run(args=cmd1_args)
            cmd2 = "chpasswd"
            cmd2_input = f"{estudante.usuario}:{estudante.matricula}"
            cmd2_args = shlex.split(cmd2)
            subprocess.run(args=cmd2_args, input=cmd2_input)

        tipos_grupos = [
                'estudante',
                'yin yang',
                'pedra papel tesoura',
                'circulo triangulo quadrado pentagono hexagono',
                'vermelho laranja amarelo verde azul anil violeta'
                ]

        for t in tipos_grupos:
            grupos = t.split()
            n_grupos = len(grupos)

            for g in grupos:
                cmd3 = f"groupadd {g}" 
                cmd3_args = shlex.split(cmd3)
                subprocess.run(args=cmd3_args)

            for i,e in enumerate(estudantes.values()):
                cmd4 = f"gpasswd -a {e.usuario} {grupos[i%n_grupos]}" 
                cmd4_args = shlex.split(cmd4)
                subprocess.run(args=cmd4_args)

if __name__ == "__main__":
    main()

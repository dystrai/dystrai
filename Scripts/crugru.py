#!/usr/bin/env python3
"""crugru: Cria usuários e grupos
"""
import argparse
import csv
from dataclasses import dataclass
import pathlib
import random
import shlex
import subprocess

@dataclass
class Estudante:
    usuario: str
    matricula: str
    nome: str
    email: str

def main():
    analisador: argparse.ArgumentParser = argparse.ArgumentParser(prog='crug')
    analisador.add_argument('csv', help='Arquivo CSV com campos ["Usuario", "Matricula", "Nome", "Email"]')
    argumentos: argparse.Namespace = analisador.parse_args()

    caminho_csv: pathlib.Path = pathlib.Path(argumentos.csv)
    if caminho_csv.exists() and caminho_csv.is_file():
        leitor: csv.DictReader = csv.DictReader(caminho_csv.open(mode='r', encoding='utf-8'))
        cabecalhos_necessarios = {'Usuario', 'Matricula', 'Nome', 'Email'}
        assert cabecalhos_necessarios.issubset(set(leitor.fieldnames)), "O arquivo CSV deve conter os campos: Usuário, Matrícula, Nome, E-mail escolar"
        estudantes = {}

        for linha in leitor:
            estudante = Estudante(linha['Usuario'], linha['Matricula'], linha['Nome'], linha['Email'])
            estudantes[estudante.usuario] = estudante

        lista_estudantes = list(estudantes.values())
        random.shuffle(lista_estudantes)
        random.shuffle(lista_estudantes)
        random.shuffle(lista_estudantes)

        for estudante in lista_estudantes:
            cmd1 = f"useradd -m -s /bin/zsh -c '{estudante.nome}' {estudante.usuario}"
            print(cmd1)
            cmd1_args = shlex.split(cmd1)
            subprocess.run(args=cmd1_args)
            cmd2 = "chpasswd"
            cmd2_input = f"{estudante.usuario}:{estudante.matricula}"
            print(f"echo {cmd2_input} | {cmd2}")
            cmd2_args = shlex.split(cmd2)
            subprocess.run(args=cmd2_args, input=cmd2_input, text=True)

        tipos_grupos = [
                'estudante',
                'yin yang',
                'pedra papel tesoura',
                'circulo triangulo quadrado pentagono hexagono',
                'vermelho laranja amarelo verde azul anil violeta',
                'alfa beta gama delta teta iota omicron sigma tau upsilon omega',
                ]

        for t in tipos_grupos:
            grupos = t.split()
            n_grupos = len(grupos)

            for g in grupos:
                cmd3 = f"groupadd {g}"
                print(cmd3)
                cmd3_args = shlex.split(cmd3)
                subprocess.run(args=cmd3_args)

            for i,e in enumerate(lista_estudantes):
                cmd4 = f"gpasswd -a {e.usuario} {grupos[i%n_grupos]}"
                print(cmd4)
                cmd4_args = shlex.split(cmd4)
                subprocess.run(args=cmd4_args)

if __name__ == "__main__":
    main()

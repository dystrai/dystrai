#!/usr/bin/env python3

"""Atribui nome de animal a cada usuário de determinada disciplina.
"""

import fire
import getpass
import pathlib
import pwd
import string
import sys

import prettytable
import yaml

class Animal:
    """Personagem animal para disciplinas com propósito de manter a identidade anônima.
    """
    def listar(self, disciplina: str, formato='tabela'):
        """Lista o usuário associado a cada um dos animais da disciplina.

        Args:
            disciplina (str): Abreviação da disciplina
            formato (str, optional): Formato da saída: tabela, csv, json. O padrão é 'tabela'.
        """
        animal_dir = pathlib.Path('/srv/disc', disciplina, 'animal', 'por-nome')
        
        if formato=='tabela':
            if animal_dir.exists() and animal_dir.is_dir():
                tabela = prettytable.PrettyTable()
                tabela.field_names = ['Animal', 'Usuário', 'Nome e matrícula do proprietário']
                tabela.align = 'l'
                for animal in animal_dir.glob('**/*'):
                    dono = animal.owner()
                    nome_dono = pwd.getpwnam(dono).pw_gecos
                    tabela.add_row([animal.name.capitalize(), dono, nome_dono])
                
                print(tabela)
    
    def reservar(self, disciplina:str, animal: str):
        """Reserva um animal para disciplina dada.

        Args:
            disciplina (str): Abreviação ou sigla da disciplina
            animal (str): Nome do animal
        """
        if not all([letra in string.ascii_lowercase for letra in animal]):
            print('O nome do animal deve ter somente letras minúsculas e sem acento.')
            return
        
        usuario = getpass.getuser()
        nome_usuario = pwd.getpwnam(usuario).pw_gecos.split(',')[0]
        prim_nome_usuario = nome_usuario.split()[0]
        
        dir_animais = pathlib.Path('/srv/disc', disciplina, 'animal')
        arq_animal_nome = dir_animais / 'por-nome' / f'{animal}'
        arq_animal_usuario = dir_animais / 'por-usuario' / f'{usuario}'

        if not arq_animal_usuario.exists():
            if arq_animal_nome.exists():
                dono = arq_animal_nome.owner()
                nome_prop = pwd.getpwnam(dono).pw_gecos.split(',')[0]
                prim_nome_prop = nome_prop.split()[0]
                if arq_animal_nome.is_file() and arq_animal_nome.owner()==usuario:
                    print(f'{prim_nome_prop}, o animal {animal} já está reservado para você em {disciplina.upper()}.')
                else:
                    print(f'''\
        {prim_nome_usuario}, sinto muito, pois o animal {animal} já foi escolhido em {disciplina.upper()} por:
        - Nome: {nome_prop}
        - Usuário {dono}
        ''')
            else:
                with arq_animal_nome.open('w', encoding='utf-8') as obj_animal_nome:
                    obj_animal_nome.write(f'{usuario}')
                with arq_animal_usuario.open(mode='w', encoding='utf-8') as obj_animal_usuario:
                    obj_animal_usuario.write(f'{animal}')
                print(f'Felicitações, {prim_nome_usuario}. O animal {animal} foi reservado para você em {disciplina.upper()}.')
        else:
            animal = arq_animal_usuario.open(encoding='utf-8').read()
            print(f'{prim_nome_usuario}, o animal {animal} já está reservado para você em {disciplina.upper()}.')
 
    def info(self, disciplina:str):
        """Obtem informações sobre o animal associado à disciplina.

        Args:
            disciplina (str): Abreviação ou sigla da disciplina
        """
        usuario = getpass.getuser()
        nome_usuario = pwd.getpwnam(usuario).pw_gecos.split(',')[0]
        prim_nome_usuario = nome_usuario.split()[0]
        
        dir_animais = pathlib.Path('/srv/disc', disciplina, 'animal')        
        arq_animal_usuario = dir_animais / 'por-usuario' / f'{usuario}'

        if arq_animal_usuario.exists():
            animal = arq_animal_usuario.open(encoding='utf-8').read()
            print(animal)
            sys.exit(0)
        else:
            print(f'{prim_nome_usuario}, não há nenhum animal associado a você em {disciplina.upper()}')
            sys.exit(1)
           
    def cancelar(self, disciplina:str):
        """Cancela o animal associado à disciplina.

        Args:
            disciplina (str): Abreviação ou sigla da disciplina
        """
        usuario = getpass.getuser()
        nome_usuario = pwd.getpwnam(usuario).pw_gecos.split(',')[0]
        prim_nome_usuario = nome_usuario.split()[0]
        
        dir_animais = pathlib.Path('/srv/disc', disciplina, 'animal')        
        arq_animal_usuario = dir_animais / 'por-usuario' / f'{usuario}'

        if arq_animal_usuario.exists():
            animal = arq_animal_usuario.open(encoding='utf-8').read()
            arq_animal_nome = dir_animais / 'por-nome' / f'{animal}'
           
            arq_animal_nome.unlink()
            arq_animal_usuario.unlink()
             
            print(f'{prim_nome_usuario}, o animal {animal} foi cancelado para você em {disciplina.upper()}.')
            
    def disciplinas(self, formato='tabela'):
        """Lista as disciplinas.
        """
        
        # TODO: Varrer diretórios em "/srv/disc"
        #       Para cada sub-diretório, abrir conteúdo do arquivo "info.yaml" (sigla, nome, ano, período, professor, curso)
        tabela = prettytable.PrettyTable()
        tabela.field_names = ['Sigla', 'Nome', 'Professor', 'Ano', 'Período']
        tabela.align = 'l'
        disc_dir = pathlib.Path('/srv/disc')
        for disc_info in disc_dir.glob('**/info.yaml'):
            dados_disc = yaml.load(disc_info.open(encoding='utf-8'), Loader=yaml.SafeLoader)
            tabela.add_row([
                dados_disc['disciplina']['sigla'],
                dados_disc['disciplina']['nome'],
                dados_disc['professor']['nome'],
                dados_disc['disciplina']['ano'],
                dados_disc['disciplina']['periodo'],
                ])
        
        print(tabela)
            

if __name__ == '__main__':
    fogo = fire.Fire(Animal())

    

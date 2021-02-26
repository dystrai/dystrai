#!/usr/bin/env python3

import getpass
import grp
import pathlib
import pwd
import subprocess
import sys

gecos = pwd.getpwnam(getpass.getuser()).pw_gecos
if ',' in gecos:
    gecos = gecos.split(',')[0]
if ' ' in gecos:
    nome = gecos.split(' ')[0]


'''
Roteiro:

# 1. Tipo do objeto
O objeto solicitado é um:
d: diretório
-: arquivo
c: disposit

# 2. Instrução de como listar as permissões

# 3. Dividir as permissões por UGO

# 4. Exibir e explicar as permissões básicas na vertical 

# 4. Exibir e explicar as permissões avançadas (set UID, set GID e stick bit)
'''

tipos_especiais = ('b', 'c', 'p', 'l', 's')
tipos = {
    '-': 'Arquivo regular',
    'd': 'Diretório',
    'b': 'Arquivo de dispositivo de bloco',
    'c': 'Arquivo de dispositivo de caractere',
    'p': 'Arquivo de pipe nomeado ou somente um pipe',
    'l': 'Arquivo de link simbólico',
    's': 'Arquivo de socket',
}

def explica_tipo(caminho: pathlib.Path, argsys: str):
    if caminho.exists():
        if caminho.is_dir():
            cmd = f'ls -ld {argsys}'
            tipo_basico = 'diretório'
            ls_ops = '-ld'
        else:
            cmd = f'ls -l {argsys}'
            tipo_basico = 'arquivo'
            ls_ops = '-l' 

        print(f'''\
{nome}, o objeto solicitado é um {tipo_basico}.
Para ver suas permissões, acrescente a oção <{ls_ops}> ao comando <ls>:
  {cmd}
''')
        usr_cmd = input('Comando: ')
        while usr_cmd != cmd:
            print(f'''\
{nome}, o objeto solicitado é um {tipo_basico}.
Para ver suas permissões, acrescente a oção <{ls_ops}> ao comando <ls>:
  {cmd}
''')
            usr_cmd = input('Comando: ')
        
        ps = subprocess.run(['/bin/ls', ls_ops, argsys], 
                            capture_output=True, 
                            text=True)
        saida = ps.stdout
        tperms,nlinks,udono,gdono,tam,mes,dia,hora,arq = saida.split(maxsplit=9)
        tipo = tperms[0]
        perms = tperms[1:]
        uperms = perms[:3]
        gperms = perms[3:6]
        operms = perms[6:]
        mgdono = grp.getgrnam(gdono).gr_mem
        print(f'{nome}, observe o tipo e permissões: {tperms}')
        print('Procure interpretá-los assim:')
        print(f'''\
 {tipo}  {uperms}  {gperms}  {operms}
 |  \_/  \_/  \_/
 0  123  456  789
 T   U    G    O

 0: Tipo ({tipo})
 123: Permissões para usuário proprietário ({udono})
 456: Permissões para membros ({','.join(mgdono)}) do grupo proprietário ({gdono})
 789: Permissões para os outros
'''
        )        
        while tlido := input('Caractere que identifica o tipo: ') != tipo:
            pass
        print(f'Certo {nome}. O tipo é: <{tipo}>')
        print(f'Isso indica que é um: {tipos[tipo]}.')
        print(f'Vamos analisar as permissões, proprietário e grupo proprietário: <{perms}>, <{udono}> e <{gdono}>.')
        while ulido := input(f'{nome}, qual é o usuário proprietário desse {tipo_basico}? ') != udono:
            pass
        while glido := input(f'{nome}, qual é o grupo proprietário desse {tipo_basico}? ') != gdono:
            pass
        print('Faremos a divisão UGO para elas.')
        while pulidas := input(f'Caracteres com permissões para o usuário <{udono}>: ') != uperms:
            pass
        print(f'Permissões para [U]suário: {uperms}')
        print('', '\n '.join(list(uperms)))
        while pglidas := input(f'Caracteres com permissões para membros do grupo <{gdono}>: ') != gperms:
            pass
        print(f'Permissões para [G]rupo: {gperms}')
        print('', '\n '.join(list(gperms)))
        while polidas := input(f'Caracteres com permissões para os outros: ') != operms:
            pass
        print(f'Permissões para [O]utros: {operms}')
        print('', '\n '.join(list(operms)))
        
        # for i,c in enumerate(tperms)
    else:
        print('Arquivo ou diretório não encontrado.')

def main():
    if len(sys.argv) != 2:
        print(f'''\
Uso:
  {sys.argv[0]} /caminho/para/arquivo-ou-diretório
''')
        sys.exit(1)
    else:
        obj = sys.argv[1]
        caminho = pathlib.Path(obj)
        explica_tipo(caminho, obj)

if __name__ == '__main__':
    main()



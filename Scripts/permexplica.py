#!/usr/bin/env python3

import getpass
import grp
import pathlib
import pwd
import subprocess
import sys
from termcolor import colored

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

class Permissao:
    def __init__(self, entidade: str, permissoes: str, tipo: str):
        assert len(permissoes) == 3
        print(permissoes)
        self._r, self._w, self._x = list(permissoes)
        self.entidade = entidade
        self.tipo = tipo

    def analisa(self):
        if self._r == 'r':
            print(f'[r]: {self.entidade} pode(m) ler.')
        elif self._r == '-':
            print(f'[-]: {self.entidade} não pode(m) ler.')
        if self._w == 'w':
            print(f'[w]: {self.entidade} pode(m) gravar/escrever.')
        elif self._w == '-':
            print(f'[-]: {self.entidade} não pode(m) gravar/escrever.')
        if self._x == 'x' and self.tipo!='d':
            print(f'[x]: {self.entidade} pode(m) executar.')
            if self.tipo == 'd':
                print(f'[x]: {self.entidade} pode(m) entrar nesse diretório.')
        elif self._x == '-':
            print(f'[-]: {self.entidade} não pode(m) executar.')            
            if self.tipo == 'd':
                print(f'[-]: {self.entidade} não pode(m) entrar nesse diretório.')
        elif self._x == 's' and self.entidade == 'u' and self.tipo == '-':
            print(f'[s]: SetUID habilitado para arquivo. O programa será executado em nome de seu proprietário.')
        elif self._x == 's' and self.entidade == 'g' and self.tipo == '-':
            print('[s]: SetGID habilitado para arquivo. O programa será executado em nome de seu grupo proprietário.')
        elif self._x == 's' and self.entidade == 'g' and self.tipo == 'd':
            print('[s]: Set GID habilitado para diretório. Os arquivos criados dentro dele pertencerão ao grupo proprietário.')
        elif self._x == 't' and self.tipo == 'd':
            print('[t]: Sticky bit habilitado para diretório. Um usuário não pode excluir o que outro criou.')

    @property
    def r(self):
        return self._r == 'r'

    @property
    def w(self):
        return self._w == 'w'

    @property
    def x(self):
        return self._x == 'x'
    

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
        print('Saída do comando:')
        print(saida)
        input('Pressione <ENTER> para continuar.')
        tperms,nlinks,udono,gdono,tam,mes,dia,hora,arq = saida.split(maxsplit=9)
        tipo = tperms[0]
        perms = tperms[1:]
        uperms = perms[:3]
        gperms = perms[3:6]
        operms = perms[6:]
        mgdono = grp.getgrnam(gdono).gr_mem
        print(f'{nome}, observe o tipo e permissões:\n {tperms}')
        print('Procure interpretá-los assim:')
        print(f'''\
 0  123  456  789            
 {colored(tipo, 'red')}  {colored(uperms, 'green')}  {colored(gperms, 'blue')}  {colored(operms, 'yellow')}
 |  \_/  \_/  \_/
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
        print('Faremos a divisão UGO para as permissões.')
        while pulidas := input(f'Caracteres com permissões para o usuário <{udono}>: ') != uperms:
            pass
        print(f'Permissões para [U]suário: {uperms}')
        print('', '\n '.join(list(uperms)))
        permissao = Permissao('u', uperms, tipo)
        permissao.analisa()
        while pglidas := input(f'Caracteres com permissões para membros do grupo <{gdono}>: ') != gperms:
            pass
        print(f'Permissões para [G]rupo: {gperms}')
        print('', '\n '.join(list(gperms)))
        permissao = Permissao('g', gperms, tipo)
        permissao.analisa()
        while polidas := input(f'Caracteres com permissões para os outros: ') != operms:
            pass
        print(f'Permissões para [O]utros: {operms}')
        print('', '\n '.join(list(operms)))
        permissao = Permissao('o', operms, tipo)
        permissao.analisa()
        
        # for i,c in enumerate(tperms)
    else:
        print('Arquivo ou diretório não encontrado.')

def main():
    if len(sys.argv) < 2:
        print(f'''\
Uso:
  {sys.argv[0]} /caminho/para/arquivo-ou-diretório
''')
        sys.exit(1)
    else:
        for arg in sys.argv[1:]:
            obj = arg
            caminho = pathlib.Path(obj)
            explica_tipo(caminho, obj)

if __name__ == '__main__':
    main()

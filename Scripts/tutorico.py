#!/usr/bin/env python3

'''
Tutorico: Pequeno tutor de um Instituto Computacional
'''

import getpass
import os
import pwd

import fire

# user = getpass.getuser()
# if not '.' in user:
#     sys.exit(1)

# nome,matricula = pwd.getpwnam(user).pw_gecos.split(',')

user = 'fulano'
nome,matricula = 'Fulano de Tal', '20219876543210'
prim_nome = nome.split(maxsplit=1)[0]
email = f'{user}@escolar.ifrn.edu.br'

class Notebook:
    def proxy(self):
        '''
        Configura um proxy do tipo Socks para acesso remoto
        '''
        # Como configurar o Jupyter Notebook com o Python 3 no Ubuntu 20.04 e se conectar via protocolo de tunelamento SSH
        # https://www.digitalocean.com/community/tutorials/how-to-set-up-jupyter-notebook-with-python-3-on-ubuntu-20-04-and-connect-via-ssh-tunneling-pt
        uid = os.getuid()
        user = getpass.getuser()
        server = 'oulu.ifrn.edu.br'
        return f'''
{prim_nome}, para executar o jupyter notebook com procuração do servidor Oulu, 
execute em sua máquina o seguinte comando:

    ssh -L {uid}:localhost:{uid} {user}@{server} meu-notebook

'''        

class ChavesSSH:
    def gerar(self):
        '''
        Gerar um par de chaves pública/privada
        '''

        return f'''
{prim_nome}, execute no cliente:        
  ssh-keygen
'''

    def listar(self):
        return '''
Execute no cliente:
  ls -1 ~/.ssh/'
'''
    def autorizadas(self):
        return f'''
{prim_nome}, execute no servidor:
  ssh-keygen -l -f .ssh/authorized_keys
'''

class EstagioSSH:

    def __init__(self):
        self.chaves = ChavesSSH()

    def reverso(self):
        reverse_port = 22000+os.getuid()
        return f'''
{prim_nome}, execute no cliente:
  ssh -R {reverse_port}:localhost:22 {user}@oulu.ifrn.edu.br'''

class EstagioGit:
    def configurar(self):
        return f'''
{prim_nome}, execute no cliente:
  git config --global user.name="{nome}"
  git config --global user.email="{email}"
'''

    def registrar(self):
        return f'''
{prim_nome}, execute no cliente:
  git add .
  git commit -m "MENSAGEM"
'''

    def estado(self):
        return 'git status'

    def enviar(self):
        return 'git push'

    def receber(self):
        return 'git pull'

class EstagioProxy:
    def socks(self):
        return 'Proxy'

class Tubulacao:
    def __init__(self):
        self.git = EstagioGit()
        self.ssh = EstagioSSH()
        self.proxy = EstagioProxy()
        self.notebook = Notebook()

class Tutorico:

    def proxy(self):
        uid = os.getuid()
        username = getpass.getuser()
        return f'ssh -L {uid}:localhost:{uid} {username}@oulu.ifrn.edu.br'

    def ssh_config(self):
        username = getpass.getuser()
        return f'''Host oulu
  Hostname oulu.ifrn.edu.br
  User {username}
  '''

if __name__ == '__main__':
    fire.Fire(Tubulacao)

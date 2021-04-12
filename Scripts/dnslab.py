#! /usr/bin/env python3

import argparse
import csv
import getpass
import ipaddress
import os
import pathlib
import pwd
import random
import subprocess
import sys
import yaml


zona_de = {
    'a.albano': 'angelica.lab',
    'adriel.teixeira': 'adriel.lab',
    'alissandra.cabral': 'alissandra.lab',
    'alves.arthur': 'arthur.lab',
    'araujo.marcio': 'marcio.lab',
    'cristiane.s': 'cristiane.lab',
    'douglas.martins': 'douglas.lab',
    'elaine.figueiredo': 'elaine.lab',
    'fulano.tal': 'fulano.lab',
    'jackeline.souza': 'jackeline.lab',
    'jonatas.marinho': 'jonatas.lab',
    'jurandy.soares': 'jurandy.lab',
    'lima.guilherme': 'guilherme.lab',
    'm.neto': 'milton.lab',
    'mateus.martins': 'mateus.lab',
    'matheus.braz': 'pereira.lab',
    'matheus.costa1': 'silva.lab',
    'r.felipe': 'felipe.lab',
    'r.isnardo': 'raquel.lab',
    'renata.chagas': 'renata.lab',
    'ricardo.a': 'ricardo.lab',
    'vidal.ricardo': 'vidal.lab',
    'vinicius.ricardo': 'vinicius.lab',
    'zanette.c': 'zanette.lab',
}


def mat2ipv6(matricula: str, ipv6_64: ipaddress.IPv6Address) -> ipaddress.IPv6Address:
    '''
    Converte matrícula para endereço IPv6
    '''

    if matricula.isdigit() and len(matricula) <= 14:
        # python - Decorating Hex function to pad zeros - Stack Overflow
        # https://stackoverflow.com/questions/12638408/decorating-hex-function-to-pad-zeros
        hexmat = '{0:#0{1}x}'.format(int(matricula), 14)[2:]
        g5,g6,g7 = hexmat[:4],hexmat[4:8],hexmat[8:]
        ipv6_grps = ipv6_64.exploded.split(':')
        ipv6_grps[4] = g5
        ipv6_grps[5] = g6
        ipv6_grps[6] = g7
        ipv6_grps[7] = '0000'

        return ipaddress.IPv6Address(':'.join(ipv6_grps))


def cria_conteiner(matricula: str, n_pc: int, ipv6_ini: ipaddress.IPv6Address):
    cmd1 = f'lxc launch images:ubuntu/20.04 pc-{n_pc}-{matricula}'
    netplan_tmpl = '''\
network:
  ethernets:
    eth0:
      addresses:
      - {end_ipv6}/64
      dhcp4: 'true'
  version: '2'
'''
    return cmd1


class DnsLab:
    def __init__(self, usuario, matricula, nome, zona, personagens):
        self.email = f'{usuario}@escolar.ifrn.edu.br'
        self.usuario = usuario
        self.matricula = matricula
        self.nome = nome
        self.zona = zona
        self.a = {p: None for p in personagens}

        # Assegure-se que os registros são únicos
        assert len(set(self.a.keys())) == len(self.a.keys())

        self.cname = {
            'ssh': personagens[0],
            'proj': personagens[1],
            'www': personagens[2],
            'bd': personagens[3],
            'arq': personagens[4],
            'ead': personagens[2],
        }

        # Assegure-se que todos os apelidos são para registros cadastrados
        for nome in self.cname.values():
            assert nome in self.a.keys()

        self.mx = {
            personagens[1]: random.randint(1, 10),
            personagens[3]: random.randint(1, 10),
        }
        # Assegure-se que os MXs são únicos
        chaves = list(self.mx.keys())
        assert chaves[0] != chaves[1]

        # Assegure-se que os MXs pertencem aos As
        assert set(self.mx.keys()).issubset(set(self.a.keys()))

    def __repr__(self):
        return f'DnsLab: <{self.nome}>'


def dados2smbtl(dados: DnsLab) -> str:
    lxdbr0 = ipaddress.IPv6Address('fd42:fcba:e07d:cd95::1')
    ipv6base = mat2ipv6(dados.matricula, lxdbr0)
    zona = dados.zona

    cmds = [f'''\
#! /bin/bash

## Conexão à Oulu
curl -s "https://oulu.ifrn.edu.br/gato/ssh?liga"
ssh {dados.usuario}@oulu.ifrn.edu.br

## Uma vez na Oulu, configure o acesso à máquina Sol com o usuário estudante.
## Se solicitado onde guardar a chave, pressione ENTER 4x

[ -f ~/.ssh/id_rsa.pub ] || ssh-keygen
ssh-copy-id estudante@sol
grep -wq sol ~/.ssh/config || storm add sol estudante@sol


# Variáveis auxiliares
ZN='{zona}.'    
NET='{str(ipv6base)[:-2]}'
AUT='-U Administrator%Ifrn.2021'
ADNS='ssh sol -- sudo samba-tool dns add localhost {zona}.'
''']

    enderecos = dados.a
    cmds.append('\n\n## AAAA: Mapeamento de nome para endereço IPv6\n')
    for i,nome in enumerate(enderecos, start=1): # É uma lista
        ip = ipv6base+(1000*6+random.randint(1, 50))
        enderecos[nome] = str(ip)
        HOST=str(ip).rsplit(':', maxsplit=1)[-1]
        fqdn = f'{nome}.$ZN'
        cmds.append(f'$ADNS {fqdn:20} AAAA $NET:{HOST} $AUT')

    cmds.append('\n\n## NS: Servidores de nome\n')
    for i,nome in enumerate(['ns1', 'ns2'], start=7): # É uma lista
        ip = ipv6base+(1000*6+random.randint(1, 50))
        enderecos[nome] = str(ip)
        HOST=str(ip).rsplit(':', maxsplit=1)[-1]
        fqdn = f'{nome}.$ZN'
        cmds.append(f'$ADNS {fqdn:20} AAAA $NET:{HOST} $AUT')
        cmds.append(f"$ADNS @ NS {nome}.$ZN $AUT")

    cmds.append('\n\n## CNAME: Associa apelido a nome canônico\n')
    for apelido,nome in dados.cname.items(): #  É um dicionário
        fqdn = f'{apelido}.$ZN'
        cname = f'{nome}.$ZN'
        cmds.append(f'$ADNS {fqdn:20} CNAME {cname:20} $AUT')        

    cmds.append('\n\n## MX: Associa servidor(es) de e-mail ao domínio\n')
    cmds.append('ssh sol')
    for mx,prior in dados.mx.items(): #  É um dicionário
        fqdn = f'{mx}.{zona}.'
        cmds.append(f'sudo samba-tool dns add localhost {zona}. @ MX "{fqdn} {prior}" -U Administrator%Ifrn.2021')

    cmds.append('\n## Pressione, 3x: Ctrl+D')

    return '\n'.join(cmds)



def main():

    usuario = getpass.getuser()
    nome,matricula = pwd.getpwnam(usuario).pw_gecos.split(',')
    prim_nome = nome.split()[0]
    slug_usr = usuario.replace('.', '-')

    md_destino = pathlib.Path(f'/var/www/html/sd20202/dnslab/{slug_usr}.md')
    pdf_destino = pathlib.Path(f'/var/www/html/sd20202/dnslab/{slug_usr}.pdf')
    url_destino = f'https://turmas.oulu.ifrn.edu.br/sd20202/dnslab/{slug_usr}.pdf'

    if md_destino.exists():
        print(f'''\
Aparentemente você já executou este comando. Visite:

- {url_destino}

''')
        sys.exit(1)
  
    # usuario = 'renata.chagas'
    # nome,matricula = 'Renata Cardoso Chagas,20171148060029'.split(',')
    
    interpretador = argparse.ArgumentParser()
    interpretador.add_argument('personagem', nargs=5)
    args = interpretador.parse_args()
    assert all([p.isalpha() for p in args.personagem])
    assert len(set(args.personagem)) == 5

    rrs = DnsLab(usuario, matricula, nome, zona_de[usuario], args.personagem)

    with open(md_destino, 'w', encoding='utf-8') as arq_md:
        sh = dados2smbtl(rrs)
        arq_md.write(f'''\
% DNS Lab. para {nome}
% Disciplina: Sistemas Distribuídos
% Professor: Jurandy Soares

# Laboratório DNS 

{prim_nome}, por gentileza, abra um terminal e execute os seguintes comandos:

```{{.bash .numberLines}}
{sh}
```

''')        

    cmd = f'pandoc -o {pdf_destino} -V geometry:landscape {md_destino}'
    ps = subprocess.run(cmd.split(), capture_output=True)

    print(f'''\
Arquivo gerado. Baixe as instruções em:

- {url_destino}

''')


if __name__ == '__main__':
    main()


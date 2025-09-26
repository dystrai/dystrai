#!/usr/bin/env python3

# A FAZER: 
# - [ ] Solicitar número do PC
# - [ ] Carregar variáveis de ambiente (Qual é o nome do PC?)
# - [ ] Solicitar o nome de um animal (Pref. aqueles que possuam emoji em Markdown)
# - [ ] Registrar presença
# - [ ] Salvar parte do nome e o animal escolhido em arquivo (YAML, JSON, INI?)

from configparser import ConfigParser
from datetime import datetime
from getpass import getuser
from pathlib import Path
from socket import gethostname
from urllib.parse import quote, urlencode
import ctypes
import os
import platform
import re
import sys
import webbrowser

# Bibliotecas externas
# Comentar as próximas 2 linhas
import requests
from unidecode import unidecode

# bibliotecas = 'requests unidecode'.split()
# bib_faltantes: list[str] = []
# for bib in bibliotecas:
#     try:
#         __import__(bib)
#     except:
#         bib_faltantes.append(bib)

# if bib_faltantes:
#     print(f'Falha ao importar a(s) biblioteca(s): {", ".join(bib_faltantes)}.')
#     print('Por gentileza, instale-a(s). Execute:')
#     print(f'\tpip install {" ".join(bib_faltantes)}')
#     sys.exit(1)

PREPOSICOES = ["de", "da", "do", "dos", "das", "e"]
URL_BANNER = "https://mange.ifrn.edu.br/ascii/arte/figlet.php"
URL_CHAMADA = "http://oulu/cgi-bin/chamada"
URL_IP = "https://mange.ifrn.edu.br/ip/"

global USUARIO
USUARIO = getuser()

global DYMON_CONF
DYMON_CONF = Path.home() / '.config' / 'dymon' / 'dymon.conf'

def saudacao() -> str:
    agora = datetime.now()
    hora = agora.hour

    return 'Bom dia' if hora <= 12 else \
           'Boa tarde' if hora < 18 else \
           'Boa noite'

def saudar(nome: str):
    cumprimento = saudacao()
    banner_cumpr = gerar_banner(f'{cumprimento},')
    banner_nome = gerar_banner(f'{nome}.')
    print(banner_cumpr)
    print(banner_nome)

def gerar_banner(texto: str) -> str:
    params = {'texto': texto}
    resp: requests.Response = requests.get(URL_BANNER, params=params)
    if resp.ok:
        return resp.text

def escolher_parte_nome(nome):
    
    partes = [parte for parte in nome.split() if parte not in PREPOSICOES]
    qt_partes = len(partes)
    opcoes = [f'{i}: {p}' for (i, p) in enumerate(partes, start=1)]
    menu = '\n'.join(opcoes)
    print('Como você gostaria de ser chamado(a)?')
    print('Digite até dois nomes, separados por espaço.')
    print(menu)

    padrao = r'^[\d]( [\d]){0,1}$'
    analops = re.compile(padrao)
    casa_padrao: bool = False
    while not casa_padrao:
        ps = input('Digite o(s) número(s): ')
        if analops.match(ps):
            casa_padrao = True
            i_partes = map(int, ps.split())
            partes_escolhidas = [unidecode(partes[i-1]).title() for i in i_partes]
    
    return ' '.join(partes_escolhidas)


# Gerado por Copilot@Windows11 em 2024-04-07
def obter_nome_completo_windows():
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)

    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    return nameBuffer.value

def salvar_nome(nome_pref: str, nome_completo: str) -> None:
    dymon_conf_dir = DYMON_CONF.parent
    os.makedirs(dymon_conf_dir, exist_ok=True)
    dymon_conf_file: Path = DYMON_CONF

    config: ConfigParser = ConfigParser()
    config['usuario'] = {}
    config['usuario']['chamar'] = nome_pref
    config['usuario']['matricula'] = USUARIO
    config['usuario']['nome'] = nome_completo
    config['usuario']['nome_preferido'] = nome_completo
    config['usuario']['hostname'] = gethostname(),

    with dymon_conf_file.open(mode='w', encoding='utf-8') as obj_dymon_conf:
        config.write(obj_dymon_conf)


def registrar_presenca_windows() -> None:
    if DYMON_CONF.exists():
        config = ConfigParser.read(DYMON_CONF)
        dados_presenca = {
            'matricula': usuario,
            'nome': nome,
            'nome_preferido': nome_pref,
            'hostname': gethostname(),
            'pc': num_pc            
        }
    else:
        usuario = getuser()
        nome = obter_nome_completo_windows()
        nome_pref = escolher_parte_nome(nome)
        salvar_nome(nome_pref=nome_pref, nome_completo=nome)
        saudar(nome_pref)

        num_pc = input('Entre com número de seu PC: ')
        while not num_pc.isdigit():
            num_pc = input('Entre com número de seu PC: ')

        dados_presenca = {
            'matricula': usuario,
            'nome': nome,
            'nome_preferido': nome_pref,
            'hostname': gethostname(),
            'pc': num_pc
        }
    dados_presenca_codificados = urlencode(dados_presenca)
    url_presenca = f'{URL_CHAMADA}?{dados_presenca_codificados}'

    # https://www.geeksforgeeks.org/how-to-open-url-in-firefox-browser-from-python-application/
    firefox = webbrowser.Mozilla("C:/Program Files/Mozilla Firefox/firefox.exe")
    firefox.open(url=url_presenca)
    

def registrar_presenca_linux():
    import pwd
    usuario = getuser()
    dados_usuario = pwd.getpwnam(usuario)
    gecos = dados_usuario.pw_gecos
    nome = gecos if ',' not in gecos else gecos.split(',')[0]
    nome_pref = escolher_parte_nome(nome)
    salvar_nome(nome_pref=nome_pref, nome_completo=nome)
    saudar(nome_pref)

def main():
    so = platform.system()
    match so:
        case 'Windows':
            registrar_presenca_windows()

        case 'Linux':
            registrar_presenca_linux()

        case _:
            print(f'O sistema operacional {so} ainda não é suportado')

if __name__ == '__main__':
    main()

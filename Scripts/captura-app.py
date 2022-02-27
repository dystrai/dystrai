#!/usr/bin/env python3

import argparse
from datetime import datetime
import pathlib
import subprocess

PROTOCOLOS = ('ftp', 'ftp-data', 'telnet', 'dns', 'smtp', 'pop3', 'imap', 'http')
DIR_CAPTURAS = '/var/www/html/capturas/'

portas_protocolo = {
    'ftp-data':  ('tcp', 20),
    'ftp':  ('tcp', 21),
    'telnet':  ('tcp', 23),
    'dns':  ('udp', 53),
    'smtp': ('tcp', 25),
    'pop3': ('tcp', 110),
    'imap': ('tcp', 143),
    'http': ('tcp', 80),
}

analisador = argparse.ArgumentParser(description='Capturador de pacotes da camada de aplicação')
analisador.add_argument('-v', '--verbose', action='store_true', help='Visualiza o que o comando irá executar')
analisador.add_argument('protocolo', nargs='+', choices=PROTOCOLOS)

args = analisador.parse_args()
regras = []
protocolos = args.protocolo
interface = 'any'
verboso = args.verbose

for proto in protocolos:
    transp,porta = portas_protocolo[proto]
    regras.append(f'{transp} port {porta}')    
    print(f'Capturando pacotes na porta {porta} do {transp.upper()}...')

filtro = ' or '.join(regras)
print(filtro)

agora = datetime.now()
nome_arq_captura = f"captura_{'_e_'.join(protocolos)}_em_{agora.strftime('%F-às-%T').replace(':', '-')}.pcap"

dir_captura = pathlib.Path(DIR_CAPTURAS)
caminho_arq_captura = dir_captura / nome_arq_captura

cmd = 'tshark'
cmd_args = [
    '-i', interface,
    '-f', f'{filtro}',
    '-c', '30',
    '-w', caminho_arq_captura.as_posix(),
]

cmd_e_args = [cmd]+cmd_args
if verboso:
    print(' '.join(cmd_e_args))

resultado = subprocess.run(cmd_e_args, stdout=subprocess.PIPE)
print(resultado)


# Usage: tshark [options] ...
#
# Capture interface:
#   -i <interface>, --interface <interface>
#                            name or idx of interface (def: first non-loopback)
#   -f <capture filter>      packet filter in libpcap filter syntax
#
# Capture stop conditions:
#   -c <packet count>        stop after n packets (def: infinite)
#
# Output:
#   -w <outfile|->           write packets to a pcapng-format file named "outfile"
#                            (or '-' for stdout)  

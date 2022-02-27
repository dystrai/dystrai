#!/usr/bin/env python3

import argparse
from datetime import datetime
import pathlib
import subprocess

DIR_CAPTURAS = '/var/www/html/capturas/'

analisador = argparse.ArgumentParser(description='Capturador de pacotes da camada de transporte')
analisador.add_argument('-v', '--verbose', action='store_true', help='Visualiza o que o comando irá executar')
analisador.add_argument('porta', type=int)
analisador.add_argument('protocolo', choices=('tcp', 'udp'))

args = analisador.parse_args()
interface = 'any'
protocolo = args.protocolo
porta = args.porta
verboso = args.verbose

filtro = f'{protocolo} port {porta}'

agora = datetime.now()
nome_arq_captura = f"captura_{protocolo}_{porta}_em_{agora.strftime('%F-às-%T').replace(':', '-')}.pcap"

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

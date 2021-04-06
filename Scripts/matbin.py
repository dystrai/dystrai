#! /usr/bin/env python3

import argparse

interpretador = argparse.ArgumentParser()
interpretador.add_argument('matricula', 
                           help='Matrícula com 14 dígitos')

argumentos = interpretador.parse_args()
matricula = argumentos.matricula

assert matricula.isdigit() and 14 == len(matricula)

matbin = '000'+bin(20181144010075)[2:]

N_FATIAS=8
matbin_fatiada = [
    matbin[N_FATIAS*i:N_FATIAS*i+N_FATIAS] 
    for i in range(len(matbin)//N_FATIAS)
    ]

matdec_fatiada = [int(fatia, base=2) for fatia in matbin_fatiada]

matbin_pontilhada = '.'.join(matbin_fatiada)
matdec_pontilhada = '.'.join(str(fatia) for fatia in matdec_fatiada)
#mathex_pontilhada = '.'.join(matbin_fatiada)

print(matbin)
print(matbin_pontilhada)
print(matdec_pontilhada)
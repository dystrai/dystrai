#! /usr/bin/env python3

import argparse
from collections import defaultdict
import ipaddress
import re
import sys

from termcolor import colored

'''
This class represents and manipulates 32-bit IPv4 network + addresses..

Attributes: [examples for IPv4Network('192.0.2.0/27')]
    .network_address: IPv4Address('192.0.2.0')
    .hostmask: IPv4Address('0.0.0.31')
    .broadcast_address: IPv4Address('192.0.2.32')
    .netmask: IPv4Address('255.255.255.224')
    .prefixlen: 27
'''

def ip2dot(end_ipv4: ipaddress.IPv4Interface):
    modelo = open('netmask.dot', 'r', encoding='utf-8').read()

    with open('/tmp/teste.dot', 'w') as arq:
	    arq.write(modelo.format(
            end_bin=end_bin, 
            masc_bin=masc_bin, 
            net_bin=rede_bin, 
            end_dec=end_dec, 
            masc_dec=masc_dec, 
            rede_dec=rede_dec)
            )

def main():
    pass

interpretador = argparse.ArgumentParser()
interpretador.add_argument('endereco_cidr', help='Endereço IPv4 com CIDR. Exemplo: 192.168.7.6/25')
args = interpretador.parse_args()


padrao_end = re.match('(?P<octeto1>\d+)\.(?P<octeto2>\d+)\.(?P<octeto3>\d+)\.(?P<octeto4>\d+)/(?P<compr_prefixo>\d+)', args.endereco_cidr)

if not padrao_end:
    sys.stderr.write('Argumento não corresponde a um endereço CIDR\n')
    sys.exit(1)

dic_cidr = padrao_end.groupdict()

octetos_dec = [int(valor) for (chave,valor) in dic_cidr.items() if chave.startswith('octeto') and 0 <= int(valor) <= 255 ]
comp_prefixo = int(dic_cidr['compr_prefixo'])
octetos_bin = []

assert 4 == len(octetos_dec)
assert 1 <= comp_prefixo <= 32

pot2 = [2**n for n in range(7, -1, -1)]


sobrescito = {
    0: '\N{SUPERSCRIPT ZERO}',
    1: '\N{SUPERSCRIPT ONE}',
    2: f'\N{SUPERSCRIPT TWO}',
    3: f'\N{SUPERSCRIPT THREE}',
    4: f'\N{SUPERSCRIPT FOUR}',
    5: f'\N{SUPERSCRIPT FIVE}',
    6: f'\N{SUPERSCRIPT SIX}',
    7: f'\N{SUPERSCRIPT SEVEN}',
}

def tabela_32bits(end_bin: str):
    print(f'+{"---+"*32}')
    print(f'| {" | ".join(end_bin)} |')
    print(f'+{"---+"*32}')

def setas_32(): 
    print("  |", "   |"*31, sep='') 
    print("  v", "   v"*31, sep='')


print(colored('Vamos converter o endereço da notação decimal pontilhada para o formato decimal?', 'blue'))
print(f'Endereço IPv4: {colored(".".join([str(o) for o in octetos_dec]), "red")}')

for i,octeto_decimal in enumerate(octetos_dec, start=1):
    print(f'\n\nValor decimal do {i}º octeto: {colored(octeto_decimal, "green")}')
    print(f'Vamos representar {colored(octeto_decimal, "green")} como soma de potências de 2?')
    resto = octeto_decimal
    fatores = []
    qtd = defaultdict(lambda:0) # Quantidade de?
    while resto > 0:
        print('Digite a maior potência de 2 para subtrair:', colored(', '.join([str(p) for p in pot2]), 'yellow'), '?')
        fator = int(input(f'Subtrair quanto de {colored(resto, "red")}: '))
        if fator > 0 and fator in pot2 and fator <= resto and fator >= (resto//2):
            resto -= fator
            fatores.append(fator)
            qtd[fator] = 1
            print(f'Resultado da subtração: ', colored('-'.join([str(octeto_decimal)]+[str(f) 
                for f in fatores])+f' = {resto}', 'red'))
        else:
            print('Fator não aceito. Tente novamente.')

    print(f'Logo, {octeto_decimal} =', colored('+'.join([str(f) for f in fatores]), 'blue'))
    print(f'Em outras "palavras", {octeto_decimal} =', colored(' + '.join([f'{qtd[p]}*{p}' for p in pot2]), 'blue'))
    print(f'Ou, {octeto_decimal} =', ' + '.join([
        colored(f'{qtd[2**n]}', "green")+'*'+colored(f'2{sobrescito[n]}', 'yellow')
        for n in range(7, -1, -1)
        ]))

    # https://stackoverflow.com/questions/16926130/convert-to-binary-and-keep-leading-zeros-in-python
    resp_binario = format(octeto_decimal, '#010b')[2:]
    octetos_bin.append(resp_binario)
    prompt = f'Como você representaria, com 8 dígitos, {colored(octeto_decimal, "red")} em binário? '
    while binario := input(prompt) != resp_binario:
        print('Resposta errada. Tente novamente.')

    print('Muito bem!')
    print(f'Já temos {i} octeto(s) transformado(s) de decimal para binário.')
    print('.'.join(octetos_bin))

print(colored('Vamos calcular agora a máscara de sub-rede...', 'blue'))
print(f'Comprimento do prefixo CIDR: {colored(str(comp_prefixo), "red")}')
resp_masc_bin = f'{"1"*comp_prefixo}{"0"*(32-comp_prefixo)}'

prompt = f'Como você representaria, no formato binário de 32 bits, a máscara com CIDR /{comp_prefixo}?\n'

masc_bin = input(prompt)
while masc_bin.replace('.', '') != resp_masc_bin:
    print('Você está quase lá. Tente novamente.')
    masc_bin = input(prompt)

octs_bin_masc = [resp_masc_bin[8*i:8*(i+1)] for i in range(4)]
octs_dec_masc = [int(oct_bin, base=2) for oct_bin in octs_bin_masc]
resp_masc_dec = '.'.join([str(dec) for dec in octs_dec_masc])

prompt = f'Como você representaria, no formato de notação decimal pontilhada, a máscara com CIDR /{comp_prefixo}?\n'
masc_dec = input(prompt)
while masc_dec != resp_masc_dec:
    print('Você está quase lá. Tente novamente.')
    masc_bin = input(prompt)

print('Estamos quase lá!')
print('Falta só você calcular: 1) O endereço de rede; 2) O endereço de broadcast.') 
print('Vamos descobrir o endereço de rede...')
print('''O endereço de rede é resultado da operação AND (E da lógica booleana)
 entre o endereço na representação binário da interface de rede e 
 o endereço na resebinário da máscara.
 ''')

print('.'.join(octetos_bin))
print('.'.join(octs_bin_masc))

if __name__ == '__main__':
    main()

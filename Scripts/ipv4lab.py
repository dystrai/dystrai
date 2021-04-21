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

endereco_cidr = args.endereco_cidr
#endereco_cidr = input('Endereço IPv4 da interface com notação CIDR: ')

padrao_end = re.match('(?P<octeto1>\d+)\.(?P<octeto2>\d+)\.(?P<octeto3>\d+)\.(?P<octeto4>\d+)/(?P<compr_prefixo>\d+)', endereco_cidr)

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

print(30*'-')
prompt = f'Como você representaria, no formato de notação decimal pontilhada, a máscara com CIDR /{comp_prefixo}?\n'
masc_dec = input(prompt)
while masc_dec != resp_masc_dec:
    print('Você está quase lá. Tente novamente.')
    masc_dec = input(prompt)

print(30*'-')
print('Estamos quase lá!')
print('Falta só você calcular: 1) O endereço de rede; 2) O endereço de broadcast.') 
print('Vamos descobrir o endereço de rede...')
print('''O endereço de rede é resultado da operação AND (E da lógica booleana)
 entre o endereço na representação binária da interface de rede e 
 o endereço binário da máscara.
 ''')

ip_bin = ''.join(octetos_bin)
masc_bin = ''.join(octs_bin_masc)

tab_inversao = str.maketrans('01', '10')
curinga_bin = str.translate(masc_bin, tab_inversao)
octs_cur_bin = [curinga_bin[8*i:8*(i+1)] for i in range(4)]

rede_int10 = int(ip_bin, 2) & int(masc_bin, 2)
rede_bin = f'{rede_int10:034b}'[2:]
octs_rede_bin = [rede_bin[8*i:8*(i+1)] for i in range(4)]
rede_dec = [int(oct_bin, base=2) for oct_bin in octs_rede_bin]

broad_int10 = int(rede_bin, 2) ^ int(curinga_bin, 2)
broad_bin = f'{broad_int10:034b}'[2:]
octs_broad_bin = [broad_bin[8*i:8*(i+1)] for i in range(4)]
broad_dec = [int(octeto, base=2) for octeto in octs_broad_bin]

print(30*'-')
while True:
    print('End. binário da Interface:', '.'.join(octetos_bin))
    print('End. binário da   Máscara:', '.'.join(octs_bin_masc))
    end_rede_bin = input('End. binário da      Rede: ')
    if end_rede_bin.replace('.', '') == rede_bin:
        print('Muito bem!')
        break

    print('Você está quase lá. Tente novamente.')

print(30*'-')
resp_rede_dec = '.'.join([str(octeto) for octeto in rede_dec])
prompt = 'Endereço da rede em notação decimal pontilhada: '
end_red_dec = input(prompt)
while end_red_dec != resp_rede_dec:
    print('Você está quase lá. Tente novamente.')
    end_red_dec = input(prompt)


print(30*'-')
print('Vamos calcular o curinga (inverter) da máscara de sub-rede?')
while True:
    print('End. binário da Máscara:', '.'.join(octs_bin_masc))
    cur_bin = input('End. inverso da Máscara: ')
    if cur_bin.replace('.', '') == curinga_bin:
        print('Muito bem!')
        break

    print('Você está quase lá. Tente novamente.')

print(30*'-')
print('Vamos descobrir o endereço de broadcast...')
print('''O endereço de broadcast é resultado da operação XOR (OU exclusivo
 da lógica booleana) entre o endereço IP da rede na representação 
 binária e curinga da máscara de sub-rede (a máscara invertida).
 ''')

while True:
    print('End. binário da      rede:', '.'.join(octs_rede_bin))
    print('End. binário do   curinga:', '.'.join(octs_cur_bin))
    end_broad_bin = input('End. binário de broadcast: ')
    if end_broad_bin.replace('.', '') == broad_bin:
        print('Muito bem!')
        break

    print('Você está quase lá. Tente novamente.')

resp_broad_dec = '.'.join([str(int(octeto, 2)) for octeto in octs_broad_bin])
prompt = 'Endereço de broadcast na notação decimal pontilhada: '
end_broad_dec = input(prompt)
while end_broad_dec != resp_broad_dec:
    print('Você está quase lá. Tente novamente.')
    end_broad_dec = input(prompt)

if __name__ == '__main__':
    main()

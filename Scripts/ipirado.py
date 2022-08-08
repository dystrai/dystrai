#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import ipaddress
import re

pontuacao_para = {
    'email': 0,
    'end_iface': 0,
    'end_rede': 0,
    'end_broadcast': 0,
    'qt_bits_redes': 0,
    'qt_bits_hosts': 0,
    'n_hosts_rede': 0,
    'end_iface_bin': 0,
    'end_iface_classe': 0,
}

def classe_ipv4_de(ip_v4: str) -> str:
    ip = [int(octeto) for octeto in ip_v4.split('.')]

    if (ip[0] >= 0 and ip[0] <= 127):
        return "A"
    
    elif(ip[0] >=128 and ip[0] <= 191):
        return "B"
    
    elif(ip[0] >= 192 and ip[0] <= 223):
        return "C"
    
    elif(ip[0] >= 224 and ip[0] <= 239):
        return "D"
    
    else:
        return "E"


leitor_csv = csv.DictReader(open('av02-respostas.csv'))
respostas_de = {linha['email']:linha for linha in leitor_csv}

# Formata as respostas
for email,respostas in respostas_de.items():
    for resp in respostas:
        respostas_de[email][resp] = respostas_de[email][resp].replace('"', '')

# respostas = {}
# for linha in leitor_csv:
#     respostas[linha['email']] = linha

expr_ipv4_bin = r"[0-1]{8}\.[0-1]{8}\.[0-1]{8}\.[0-1]{8}"
padrao_ipv4_bin = re.compile(expr_ipv4_bin)

def comp_enderecos_binarios(ender1: str, ender2: str) -> int:
    assert (len(padrao_ipv4_bin.findall(ender1))==1) and len(padrao_ipv4_bin.findall(ender2))==1
    
    ender1_lst = list(ender1)
    ender2_lst = list(ender2)
    diff_end_1e2 = [bit_ender1==bit_ender2 for bit_ender1,bit_ender2 in zip(ender1_lst,ender2_lst)]
    print(ender1, ender2, sep='\n')
    print(''.join([' ' if valor else '|' for valor in diff_end_1e2]))
    return diff_end_1e2.count(False)

def analisa_ip(ip_cidr: str):
    ip,prefixo = ip_cidr.split('/')
    iface = ipaddress.ip_interface(ip_cidr)
    net = iface.network

    print(f'Rede: {net}')
    print(f'Broadcast: {net.broadcast_address}/{prefixo}')
    print(f'Número de dispositivos: {net.num_addresses-2}')
    octetos_dec = ip.split(".")
    octectos_bin = [f'{int(x):08b}' for x in octetos_dec]
    end_iface_bin = '.'.join(octectos_bin)
    print(f'Binário: {end_iface_bin}')
    bin2compare = input('Binário para comparar: ')
    print(end_iface_bin, bin2compare, sep='\n')
    print('Iguais:', bin2compare==end_iface_bin)
    comp_enderecos_binarios(end_iface_bin, bin2compare)
    classe_ipv4 = classe_ipv4_de(ip)
    print(f'Classe: {classe_ipv4}')


while ip_cidr := input('Endereço IP na notação CIDR: '):
    analisa_ip(ip_cidr)
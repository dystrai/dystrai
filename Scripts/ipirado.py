#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress

iface = ipaddress.ip_interface("188.184.7.219/27")

type(iface)
dir(iface)

net = iface.network
type(net)
dir(net)
print(net)

len(list(net.hosts()))

for host in net.hosts():
    print(host)

for i,host in enumerate(net.hosts(), start=1):
    print(f'Host {i}: {host}')

print(net.broadcast_address)

matricula = 2020987654321
print(f'Minha matrícula é {matricula} na notação decimal.')
print(f'Minha matrícula é {matricula:b} na notação binária.')
print(f'Minha matrícula é {matricula:x} na notação hexadecimal.')

octetos_dec = '188.184.7.223'.split(".")
print(octetos_dec)

octectos_bin = [f'{int(x):08b}' for x in octetos_dec]
print('.'.join(octectos_bin))

octs_bin = "10001110.01100000.01000111.10111010".split('.')
octs_dec = [int(x, 2) for x in octs_bin]
print('.'.join([str(y) for y in octs_dec]))

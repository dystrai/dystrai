#! /usr/bin/env python3

import argparse
from random import randint
import ipaddress


def gera_ipv4(prefix_len: int) -> str:

    oct1 = randint(1, 223) # Restrito às classes A, B e C
    oct2 = randint(0, 255)
    oct3 = randint(0, 255)
    oct4 = randint(0, 255)

    ipv4 = f'{oct1}.{oct2}.{oct3}.{oct4}/{prefix_len}'
    return ipv4

def gera_ipv4_valido(prefix_len: int) -> str:
    """Gera endereço IPv4 válido

    Args:
        prefix_len (int): Comprimento do prefixo

    Returns:
        str: Um endereço IPv4 válido na notação decimal pontilhada no formato CIDR
    """    
    while True:
        ipv4 = gera_ipv4(prefix_len)
        iface = ipaddress.IPv4Interface(ipv4)
        netaddr = str(iface.network).split('/')[0]
        broadaddr = str(iface.network.broadcast_address)

        if ipv4 not in (netaddr, broadaddr):
            break

    return ipv4

if __name__ == '__main__':
    interpretador = argparse.ArgumentParser()
    interpretador.add_argument('--barra', required=False, type=int)
    global args
    args = interpretador.parse_args()
    comprimento_prefixo = args.barra if args.barra else randint(0, 32)
    print(gera_ipv4_valido(comprimento_prefixo))


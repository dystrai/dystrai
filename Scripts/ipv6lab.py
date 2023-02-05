import ipaddress
from typing import Union

def mat2ipv6(matricula: Union[str, int], ipv6netaddr: ipaddress.IPv6Network) -> ipaddress.IPv6Address:
    """Gera endereço IPv6 baseado em matrícula

    Args:
        matricula (str): Matrícula do IFRN com 14 dígitos
        ipv6netaddr (ipaddress.IPv6Network): Endereço de uma rede IPv6

    Returns:
        ipaddress.IPv6Address: Endereço IPv6 com resultado da soma entre o endereço de rede a matrícula representada por 64 bits.
    """

    if str(matricula).isdigit():
        hexmat = f'{hex(int(matricula))[2:]}'.zfill(12)
        hexadecatetos = (
            hexmat[:4],
            hexmat[4:8],
            hexmat[8:],
            '0000'
            )

        return ipv6netaddr.network_address+int((''.join(hexadecatetos)), 16)+1

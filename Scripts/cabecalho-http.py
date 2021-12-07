#!/usr/bin/env python4

import re
import requests
import sys
from urllib.parse import urlparse
import yaml

def exibir_cabecalho(url) -> str:
    ana_url = urlparse(url)
    if ana_url.scheme in ('http', 'https') and ana_url.netloc:
        resp = requests.get(url)
        return yaml.dump(dict(resp.headers))
    
    return ''

print(sys.argv)

if len(sys.argv) > 1:
    for url in sys.argv[1:]:
        print(exibir_cabecalho(url))
else:
    while url := input('Entre com uma URL (Pressione Enter e uma URL vazia para SAIR): '):
        print(exibir_cabecalho(url))

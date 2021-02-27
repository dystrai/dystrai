#!/usr/bin/env python3

import subprocess
import sys
from urllib.parse import urlparse, parse_qs

pt_cabecalho_resp = {
    'Date': 'Data',
    'Server': 'Servidor',
    'Last-Modified': 'Última-Modificação',
    'ETag': 'Etiqueta-eletrônica',
    'Accept-Ranges': 'Aceitar-Intervalos',
    'Content-Length': 'Comprimento-do-Conteúdo',
    'Vary': 'Variar',
    'Content-Type': 'Tipo-de-conteúdo',
}

class ReqResp:
    def __init__(self, linha, cabecalho):
        self.linha = linha
        self.cabecalho = cabecalho

    def __str__(self):
        ENTER = '\n'
        return f'''{self.linha}
{ENTER.join(self.cabecalho)}
'''        

class Requisicao(ReqResp):
    def __init__(self, linha, cabecalho):
        super().__init__(linha, cabecalho)

class Resposta(ReqResp):
    def __init__(self, linha, cabecalho):
        super().__init__(linha, cabecalho)
        self._traduz_cabecalho()

    def _traduz_cabecalho(self):
        traducao = []
        for linha in self.cabecalho:
            chave,valor = linha.split(':', maxsplit=1)
            if chave in pt_cabecalho_resp:
                traducao.append(':'.join([pt_cabecalho_resp[chave], valor]))
            else:
                traducao.append(linha)
        self.cabecalho_traduzido = traducao

    def cadeia_cabecalho_traduzido(self):
        ENTER = '\n'
        return f'''{self.linha}
{ENTER.join(self.cabecalho_traduzido)}
'''

def separador_req_resp(url: str):
    ps = subprocess.run(['curl', '-v', url], 
                        capture_output=True, 
                        text=True,
                        check=True)
    linhas_req = []
    linhas_resp = []
    for linha in ps.stderr.splitlines():
        if linha.startswith('> '):
            linhas_req.append(linha[2:])
        elif linha.startswith('< '):
            linhas_resp.append(linha[2:])
    
    requisicao = Requisicao(linhas_req[0], linhas_req[1:-1])
    resposta = Resposta(linhas_resp[0], linhas_resp[1:-1])
        
    return (requisicao, resposta)


porta_padrao = {
    'http': 80,
    'https': 443,
}

def analisa_url(url: str):
    analise = urlparse(url)
    print('Esquema (scheme):', analise.scheme)
    print('Host:', analise.hostname)
    if analise.port:
        print('Porta:', analise.port)
    else:
        print('Porta:', porta_padrao[analise.scheme])
    print('Caminho (path):', analise.path)
    print('Consulta (query string):', analise.query)
    print('Fragmento:', analise.fragment)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        analisa_url(url)
        req,resp = separador_req_resp(url)
        print('REQUISIÇÃO:')
        print(req)
        print()
        print('RESPOSTA:')
        print(resp.cadeia_cabecalho_traduzido())

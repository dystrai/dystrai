#!/usr/bin/env python3

import subprocess
import sys
from urllib.parse import urlparse, parse_qs

ENTER = '\n'

pt_cabecalho_resp = {
    'Accept-Ranges': 'Aceitar-Intervalos',
    'Content-Length': 'Comprimento-do-Conteudo',
    'Content-Type': 'Tipo-de-conteudo',
    'Date': 'Data',
    'ETag': 'Etiqueta-eletronica',
    'Last-Modified': 'Ultima-Modificacao',
    'Location': 'Localizacao',
    'Server': 'Servidor',
    'Vary': 'Variar',
}

class AbsReqResp:
    def __init__(self, linha, cabecalho):
        self._linha = linha
        self._cabecalho = cabecalho

    @property
    def linha(self):
        return self._linha
    
    @property
    def cabecalho(self):
        return ENTER.join(self.cabecalho)

    def __str__(self):
        return ENTER.join([self.linha, self.cabecalho])

class Requisicao(AbsReqResp):
    def __init__(self, linha, cabecalho):
        super().__init__(linha, cabecalho)


    # https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html
    def como_markdown(self):
        return f'''\

- Linha de requisição:

  `{self.linha}`

- Análise da linha de requisição:

  | Método | URI Requisitada | Protocolo/versão |
  | ------ | --------------- | -----------------|
  | {' | '.join(self.linha.split())} |

- Cabeçalho de requisição

  ```yaml
  {(ENTER+'  ').join(self._cabecalho)}            
  ```
'''

class Resposta(AbsReqResp):
    def __init__(self, linha, cabecalho):
        super().__init__(linha, cabecalho)
        self._traduz_cabecalho()

    def _traduz_cabecalho(self):
        traducao = []
        for linha in self._cabecalho:
            chave,valor = linha.split(':', maxsplit=1)
            if chave in pt_cabecalho_resp:
                traducao.append(':'.join([pt_cabecalho_resp[chave], valor]))
            else:
                traducao.append(linha)
        self._cabecalho_traduzido = traducao

    @property
    def cabecalho_traduzido(self):
        return ENTER.join(self.cabecalho_traduzido)

    def como_markdown(self):
        return f'''\
- Linha de resposta:

  `{self.linha}`

- Análise da linha de resposta:

  | Protocolo/versão | Código de retorno | Mensagem |
  | ---------------- | ----------------- | -------- |
  | {' | '.join(self.linha.split(maxsplit=3))} |

- Cabeçalho de resposta

  ```yaml
  {(ENTER+'  ').join(self._cabecalho)}            
  ```

- Tradução (parcial) do cabeçalho de resposta

  ```yaml
  {(ENTER+'  ').join(self._cabecalho_traduzido)}            
  ```

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

def analisa_url(url: str) -> str:
    analise = urlparse(url)
    porta = analise.port if analise.port else porta_padrao[analise.scheme]
        
    return f'''\
| Chave | Valor |
| ----- | ----- |
| Esquema (scheme) |  {analise.scheme} |
| Host |  {analise.hostname} |
| Porta | {porta} |
| Caminho (path) |  {analise.path} |
| Consulta (query string) | {analise.query} |
| Fragmento |  {analise.fragment} |

'''

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]

        print('# Laboratório HTTP')
        print()
        print(f'- URL: \<<{url}>\>')
        print ('## Análise da URL')
        print(analisa_url(url))

        req,resp = separador_req_resp(url)

        print('## Análise da requisição')
        print(req.como_markdown())

        print('## Análise da resposta')    
        print(resp.como_markdown())


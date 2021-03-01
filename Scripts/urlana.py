#!/usr/bin/env python3

import subprocess
import sys
from urllib.parse import urlparse, parse_qs

ENTER = '\n'

pt_cabecalho_resp = {
    'Accept-Ranges': 'Aceitar-Intervalos',
    'Connection': 'Conexão',
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
        return ENTER.join(self._cabecalho)

    def __str__(self):
        return ENTER.join([self.linha, self.cabecalho])

class Requisicao(AbsReqResp):
    def __init__(self, linha, cabecalho):
        linha = ' '.join(['GET', linha.split(maxsplit=1)[1]])
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
  {(ENTER+'  ').join(self._cabecalho).replace('Accept: */*', 'Accept: "*/*"')}            
  ```

  ```{{note}}
  O valor associado ao campo **Accept:** foi exibido entre aspas duplas 
  para que o cabeçalho de requisição pudesse ser destacado como um arquivo 
  no formato [YAML](https://yaml.org/).
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
        return ENTER.join(self._cabecalho_traduzido)

    def como_markdown(self):
        return f'''\
- Linha de resposta:

  `{self.linha}`

- Análise da linha de resposta:

  | Protocolo/versão | Código de retorno | Mensagem |
  | ---------------- | ----------------- | -------- |
  | {' | '.join(self.linha.split(maxsplit=2))} |

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

    ps = subprocess.run(['curl', '-I', '-v', url], 
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

class URL:
    def __init__(self, url: str):
        self._url = url.strip()
        self._analisa()

    @property
    def nome(self):
        return self._url

    def _analisa(self):
        analise = urlparse(self._url)
        self.porta = analise.port if analise.port else porta_padrao[analise.scheme]
        self.caminho = analise.path.strip() if analise.path else '/'
        self.esquema   = analise.scheme
        self.loc_rede   = analise.netloc
        self.parametros   = analise.params
        self.consulta    = analise.query
        self.fragmento = analise.fragment
        self.usuario = analise.username
        self.senha = analise.password
        self.computador = analise.hostname

    def como_tabela_markdown(self):
        return f'''\
| Chave | Valor |
| ----- | ----- |
| Esquema (scheme) |  {self.esquema} |
| Computador |  {self.computador} |
| Porta | {self.porta} |
| Caminho (path) |  {self.caminho} |
| Consulta (query string) | {self.consulta} |
| Fragmento |  {self.fragmento} |
'''

    def __str__(self):
        return self._url

    def __repr__(self):
        return self._url

def req_resp_como_puml(vc: str, req: Requisicao, resp: Resposta, url: URL):
    return f'''\
```{{uml}}        
@startuml
actor "{vc}" as vc
participant "Navegador Web" as nav
participant "{url.computador}:{url.porta}" as host
vc -> nav: {url}
nav -> host: {req.linha}
note left
{req.cabecalho}
end note
host -> nav: {resp.linha}
note right
{req.cabecalho}
end note
nav -> nav: Vou analisar a resposta
note left
Se for um documento HTML,
preciso solicitar mais objetos
(Ex.: CSS, JavaScript, imagens)
para <{url.computador}> ou outros
hosts, dependendo da análise.
end note
nav -> vc: Página linda, maravilhosa e perfurmada
@enduml
```
'''        
    

if __name__ == '__main__':
    pass

if len(sys.argv) == 4:
    vc = sys.argv[1]
    ordem = sys.argv[2]
    url = URL(sys.argv[3])
    req,resp = separador_req_resp(url.nome)    

    print(f'# Lab. HTTP -- Análise {ordem} para {vc}')
    print(f'- URL: \<<{url.nome}>\>')

    print('## Diagrama')
    print(f'''Vamos ver um diagrama de sequência com a interação entre:

1. Você {vc},
2. Seu navegador web predileto (Chrome, Edge, Firefox, Opera, Safari etc.), e
3. O servidor (*{url.loc_rede}*) que hospeda o objeto solicitado (*{url.caminho}*).
''')
    print(req_resp_como_puml(vc, req, resp, url))

    print ('## A URL')
    print()
    print(url.como_tabela_markdown())

    print('## Request')
    print('Vamos analisar a requisição.')
    print(req.como_markdown())

    print('## Response')    
    print('Vamos analisar a resposta.')
    print(resp.como_markdown())


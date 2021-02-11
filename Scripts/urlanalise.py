from urllib.parse import urlparse, parse_qs

while url := input('URL: '):
    resultado = urlparse(url)
    print('Esquema:', resultado.scheme)
    print('Host:', resultado.hostname)
    print('Porta:', resultado.port)
    print('Caminho:', resultado.path)
    print('Consulta:', resultado.query)
    print('Fragmento:', resultado.fragment)




#!/usr/bin/env python3

from getpass import getuser
import pwd
import unicodedata

def utf8_para_ascii(cadeia: str) -> str:
    return unicodedata.normalize('NFKD', cadeia).encode('ASCII', 'ignore').decode('utf-8')

prep_port = 'e de da do de das dos'.split()

# nome = 'Fulano de Tal Pereira da Silva'

# TODO: Transformar nome da codificação UTF-8 para ASCII

# Opção 1: Ler os dados do usuário ou receber como argumento via linha de comandos
# nome = input('Seu nome completo: ') if (len(sys.argv) != 2) else sys.argv[1]

# Opção 2: Extrair os dados da conta do usuário no Unix/Linux
usuario = getuser()
dados_usuario = pwd.getpwnam(usuario)
nome,matricula = dados_usuario.split(',')

nome_quebrado = utf8_para_ascii(nome).title().split()

palavras_selecionadas = [ palavra
    for palavra in nome_quebrado 
        if palavra.lower() not in prep_port
        ]

cabecalho = 'Letra,Bit1,Bit2,Bit3,Bit4,Bit5,Bit6,Bit7,Bit8,BitParidade'

for palavra in palavras_selecionadas:
    with open(f'{palavra.lower()}.csv', mode='w', encoding='utf-8') as arq_csv:
        arq_csv.write(f'{cabecalho}\n')
        
        for letra in palavra:
            cod_dec_letra = ord(letra)
            cod_bin_letra = f'{cod_dec_letra:08b}'
            linha_arq = [letra] + list(cod_bin_letra) + ['_']
            arq_csv.write(f'{",".join(linha_arq)}\n')
        
        # Escreve mais uma linha, para paridade de coluna
        ult_linha = 10*['_']
        ult_linha[0] = 'Paridade'
        arq_csv.write(f'{",".join(ult_linha)}\n')
        

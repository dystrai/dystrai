#! /usr/bin/env python3

import getpass
import sys

usuario = getpass.getuser()

class MiniCabecalhoTCP:
    def __init__(self, hostname: str, seq_ini: int):
        self.hostname = hostname
        self.seq = seq_ini
        self.ack = 0

    def enviar(self, nbytes: int, outro_cabecalho):
        outro_cabecalho.ack = self.seq+nbytes
        resultado = f'{self.hostname} -> {outro_cabecalho.hostname}: seq={self.seq}\\nack={self.ack}\\nEnviado {nbytes} bytes'
        self.seq = outro_cabecalho.ack

        return resultado


class MiniTCP:
    def __init__(self):
        pass

    def conectar(self):
        pass

    def transferir(self):
        pass

    def desconectar(self):
        pass



def main():
    # cliente = input('Nome do computador cliente (somente letras): ')
    # while not cliente.isalpha():
    #     cliente = input('Nome do cliente (somente letras): ')
    # cli_seq_ini = int(input(f'Valor inicial de SEQ para {cliente}: '))

    # servidor = input('Nome do servidor (somente letras): ')
    # while not servidor.isalpha():
    #     servidor = input('Nome do servidor (somente letras): ')
    # srv_seq_ini = int(input(f'Valor inicial de SEQ para {servidor}: '))

    cliente = 'uno'
    cli_seq_ini = 15 
    servidor = 'duno'
    srv_seq_ini = 18

    cabecalho_hosts = (
                    MiniCabecalhoTCP(cliente, cli_seq_ini), 
                    MiniCabecalhoTCP(servidor, srv_seq_ini)
                    )

    mss = int(input('Tamanho máximo de segmento (MSS): '))
    mensagem = input('Mensagem a ser transmitida (sem acento): ')

    # transmissoes = map(int, input('Sequência de bytes a transmitir: ').split())
    transmissoes = (20, 30, 15, 17, 18, 20, 15)

    for i,b in enumerate(transmissoes):
        print(cabecalho_hosts[(i)%2].enviar(b, cabecalho_hosts[(i+1)%2]))


if __name__ == '__main__':
    main()
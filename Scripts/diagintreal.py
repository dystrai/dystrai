class Intervalo:
    def __init__(self, ini:  int, fim: int) -> None:
        assert fim > ini
        
        self.ini = ini
        self.fim = fim
        self._comprimento = fim-ini
        
    @property
    def comprimento(self):
        return self._comprimento
        
    def desenha_regua(self, larg_uni: int, caracter: str='-'):
        marcacoes = ['|']*(self.comprimento+1)
        print((larg_uni*caracter).join(marcacoes))
        
        print(self.ini, end='')#(larg_uni*caracter))
        for num in range(self.ini+1, self.fim+1):
            str_num = str(num)
            print(str_num.rjust(larg_uni+1, ' '), end='')
        print()

    def desenha_intervalo_real(self, ini: int, fim: int, larg_uni: int):
        assert ini>=self.ini and fim<=self.fim
        print(' '*((larg_uni+1)*ini), end=' ')
        print('x'*((larg_uni+1)*(fim-ini)), end='\b ')
        
if __name__ == '__main__':    
    intervalo = Intervalo(0, 30)
    intervalo.desenha_regua(5)
    intervalo.desenha_intervalo_real(3, 11, 5)

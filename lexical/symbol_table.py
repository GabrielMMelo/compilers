

class TabelaSimbolos:

    def __init__(self):
        self.tabela = []
    '''
    def __str__(self):
        # TODO 
    '''
    def add(self, valor):
        if valor not in self.tabela:
            self.tabela.append(valor)
        return self.tabela.index(valor)

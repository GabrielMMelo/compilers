class TabelaSimbolos:
    def __init__(self):
        self.tabela = []

    def __str__(self):
        retorno = '\nTabela de Simbolos:\n'
        for idx, val in enumerate(self.tabela):
            retorno += "ID: " + str(idx) + ", Valor: " + str(val) + "\n"
        return retorno

    def add(self, valor):
        if valor not in self.tabela:
            self.tabela.append(valor)
        return self.tabela.index(valor)

    def remove_last(self):
        del self.tabela[-1]

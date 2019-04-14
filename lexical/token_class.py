

class Token:

    def __init__(self, tipo, valor, linha, coluna, indiceTabelaSimbolo=None):
        self.tipo = tipo
        self.valor = valor
        self.indiceTabelaSimbolo = indiceTabelaSimbolo
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        if self.indiceTabelaSimbolo is not None:
            return "<{}, {}, {}, {}>".format(self.tipo, self.indiceTabelaSimbolo, self.linha, self.coluna)
        else:
            return "<{}, '{}', {}, {}>".format(self.tipo, self.valor, self.linha, self.coluna)

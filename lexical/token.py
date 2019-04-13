from Lexemas import Lexemas


class Token:

    def __init__(self, tipo, valor, linha, coluna, indiceTabelaSimbolo=None):
        self.tipo = tipo
        self.valor = valor
        self.indiceTabelaSimbolo = indiceTabelaSimbolo
        self.linha = linha
        self.coluna = coluna

    def __str__(self):
        strTipo = str(self.tipo)
        strTipo = strTipo.split('.')[1]  # ira ignorar o Lexemas.
        if self.indiceTabelaSimbolo is not None:
            return "<{}, {}, {}, {}>".format(strTipo, self.indiceTabelaSimbolo, self.linha, self.coluna)
        else:
            return "<{}, {}, {}, {}>".format(strTipo, self.valor, self.linha, self.coluna)

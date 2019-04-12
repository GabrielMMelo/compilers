from Lexemas import Lexemas

class Token:

    def __init__(self, tipo, valor, linha, coluna, indiceTabelaSimbolo = None): 
        self.tipo = tipo
        self.valor = valor
        self.indiceTabelaSimbolo = indiceTabelaSimbolo
        self.linha = linha
        self.coluna = coluna
    
    def __str__(self):
        strTipo = str(self.tipo)
        strTipo = strTipo.split('.')[1] #irá ignorar o Lexemas.
        if self.indiceTabelaSimbolo != None:
            return "<" + strTipo + ", " + str(self.indiceTabelaSimbolo) + ", " + str(self.linha) + ", " + str(self.coluna) + ">"
        else:
            return "<" + strTipo + ", " + self.valor + ", " + ", " + str(self.linha) + ", " + str(self.coluna) + ">"

from lexical.lexeme import Lexemas

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.actual = 0       # posição da lista de tokens
        self.success = False  # indicador da tradução correta
        self.errors = []      # faremos detecção de erros?

    def see_actual_token(self):
        return self.tokens[self.actual]

    def move_token_foward(self):
        self.actual += 1
        if self.actual == len(self.tokens):
            self.success = True

    def match(self, token):
        try:
            if self.tokens[self.actual].tipo == Lexemas.lexema[token]:
                self.move_token_foward()
                return True
        except KeyError:
            if self.tokens[self.actual].tipo == token:  # caso seja um identificador
                self.move_token_foward()
                return True
        return False
        # throw a error here!

    def analisar(self):
        self.programa()
        if self.success:
            print("success")

    def programa(self):
        self.declaracaoLista()

    def declaracaoLista(self):
        self.declaracao()
        #  while not self.success:  # repensar isso
        #     self.declaracao()

    def declaracao(self):
        if self.var_declaracao():  # DEFINIR COMO UTILIZAR O RETORNO
            pass
        else:
            self.fun_declaracao()

    def fun_declaracao(self):
        pass

    def var_declaracao(self):
        self.tipo_especificador()  # DEFINIR COMO UTILIZAR O RETORNO
        self.ident()  # DEFINIR COMO UTILIZAR O RETORNO
        result = self.match(';')
        return result
        # finalizar função...

    def tipo_especificador(self):
        pass

    def ident(self):
        pass

from lexical.lexeme import Lexemas


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.actual = 0       # posição da lista de tokens
        self.success = False  # indicador da tradução correta
        self.errors = []      # faremos detecção de erros?
        self.expressions = []

    def imprimir_erros(self):
        if not self.errors:
            return
        print("Erros:")
        for e in self.errors:
            print(e)

    def see_actual_token(self):
        return self.tokens[self.actual]

    def move_token_forward(self):
        self.actual += 1
        if self.actual == len(self.tokens):
            self.success = True

    def move_token_backward(self, number=None):
        self.actual = number

    def match(self, token):
        try:
            if self.tokens[self.actual].tipo == Lexemas.lexema[token]:
                self.move_token_forward()
                return True
        except KeyError:
            if self.tokens[self.actual].tipo == token:  # caso seja um identificador
                self.move_token_forward()
                return True
        return False
        # throw a error here!

    def analisar(self):
        return self.programa()

    def programa(self):
        return self.declaracaoLista()

    def declaracaoLista(self):
        if self.declaracao():
            while self.declaracao():
                pass
            return self.success  # Verifica se leu todos os tokens
        self.errors.append("Não foi feita nenhuma declaração. Linha: {}, Coluna: {}".format(
            self.tokens[self.actual].linha, self.tokens[self.actual].coluna))
        return False

    def declaracao(self):
        if self.success:
            return False

        # É necessário guardar a possição atual para caso ocorra erro
        # poder voltar os tokens que foram lidos.
        actual_index = self.actual
        if self.var_declaracao():
            return True

        self.move_token_backward(actual_index)

        if self.fun_declaracao():
            return True

        self.errors.append("Não foi feita nenhuma declaração de variável ou função. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def var_declaracao(self):
        actual_index = self.actual
        if self.tipo_especificador():
            if self.ident():
                if self.match(';'):
                    return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.tipo_especificador():
            if self.ident():
                if self.match('['):
                    if self.num_int():
                        if self.match(']'):
                            while self.match('[') and self.num_int() and self.match(']'):
                                pass
                            if self.match(';'):
                                return True

        self.move_token_backward(actual_index)
        self.errors.append("Variável declarada incorretamente. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def tipo_especificador(self):
        if self.match('INT'):
            return True
        if self.match('FLOAT'):
            return True
        # A descrição do trabalho está incorreta. Não é possível identificar char
        # if self.match('CHAR'):
        #    return True
        if self.match('VOID'):
            return True
        actual_index = self.actual
        if self.match('STRUCT'):
            if self.ident():
                if self.match('{'):
                    if self.atributos_declaracao():
                        if self.match('}'):
                            return True

        self.move_token_backward(actual_index)
        self.errors.append("Tipo especificador inesperado. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def atributos_declaracao(self):
        actual_index = self.actual
        if self.var_declaracao():
            while self.var_declaracao():
                pass
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração de atributos inválido. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def fun_declaracao(self):
        actual_index = self.actual
        if self.tipo_especificador():
            if self.ident():
                if self.match('('):
                    if self.params():
                        if self.match(')'):
                            if self.composto_decl():
                                return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração de função inválida. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def params(self):
        actual_index = self.actual
        if self.match('VOID'):
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.param_lista():
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Parâmetros inválidos. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def param_lista(self):
        actual_index = self.actual
        if self.param():
            notEnd = True
            while notEnd:
                actual_index = self.actual
                notEnd = self.match(',')
                if notEnd:
                    if not self.param():
                        self.move_token_backward(actual_index)
                        notEnd = False
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Lista de parâmetros inválida. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    # alterei a ordem das derivações da gramatica p/ rodar
    def param(self):
        actual_index = self.actual
        if self.tipo_especificador():
            if self.ident():
                if self.match('['):
                    if self.match(']'):
                        return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.tipo_especificador():
            if self.ident():
                return True

        self.move_token_backward(actual_index)
        self.errors.append("Parâmetro inválido. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def composto_decl(self):
        actual_index = self.actual
        if self.match('{'):
            if self.local_declaracoes():
                if self.comando_lista():
                    if self.match('}'):
                        return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def local_declaracoes(self):
        notEnd = True
        while notEnd:
            actual_index = self.actual
            if not self.var_declaracao():
                self.move_token_backward(actual_index)
                notEnd = False

        return True

    def comando_lista(self):
        notEnd = True
        while notEnd:
            actual_index = self.actual
            if not self.comando():
                self.move_token_backward(actual_index)
                notEnd = False

        return True

    def comando(self):
        actual_index = self.actual
        if self.expressao_decl():
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.composto_decl():
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.selecao_decl():
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.iteracao_decl():
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.retorno_decl():
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de comandos. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def expressao_decl(self):
        actual_index = self.actual
        if self.expressao():
            if self.match(';'):
                return True
        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.match(';'):
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de expressão. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    # alterei a ordem das derivações da gramatica p/ rodar
    def selecao_decl(self):
        actual_index = self.actual
        if self.match('IF'):
            if self.match('('):
                if self.expressao():
                    if self.match(')'):
                        if self.comando():
                            if self.match('ELSE'):
                                if self.comando():
                                    return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.match('IF'):
            if self.match('('):
                if self.expressao():
                    if self.match(')'):
                        if self.comando():
                            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de condicional. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def iteracao_decl(self):
        actual_index = self.actual
        if self.match('WHILE'):
            if self.match('('):
                if self.expressao():
                    if self.match(')'):
                        if self.comando():
                            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de iteração. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def retorno_decl(self):
        actual_index = self.actual
        if self.match('RETURN'):
            if self.match(';'):
                return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.match('RETURN'):
            if self.expressao():
                if self.match(';'):
                    return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de retorno. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def expressao(self):
        actual_index = self.actual
        if self.var():
            if self.match('='):
                if self.expressao():
                    self.expressions.append(actual_index)
                    return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.expressao_simples():
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Expressão inválida. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    # alterei a ordem das derivações da gramatica p/ rodar
    def var(self):
        actual_index = self.actual
        if self.ident():
            if self.match('['):
                if self.expressao():
                    if self.match(']'):
                        while self.match('[') and self.expressao() and self.match(']'):
                            pass
                        return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.ident():
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de váriavel. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def expressao_simples(self):
        actual_index = self.actual
        if self.expressao_soma():
            if self.relacional():
                if self.expressao_soma():
                    return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.expressao_soma():
            return True

        self.move_token_backward(actual_index)
        return False

    def relacional(self):
        if self.match('<='):
            return True
        if self.match('<'):
            return True
        if self.match('>'):
            return True
        if self.match('>='):
            return True
        if self.match('=='):
            return True
        if self.match('!='):
            return True
        self.errors.append("Declaração inválida de operador lógico. Linha: {}, Coluna: {}".format(
            self.tokens[self.actual].linha, self.tokens[self.actual].coluna))
        return False

    def expressao_soma(self):
        actual_index = self.actual
        if self.termo():
            notEnd = True
            while notEnd:
                notEnd = self.soma()
                if notEnd:
                    actual_index = self.actual
                    if not self.termo():
                        self.move_token_backward(actual_index)
                        notEnd = False
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de expressão (+/-). Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def soma(self):
        if self.match('+'):
            return True
        if self.match('-'):
            return True
        self.errors.append("Declaração inválida de operador (+/-). Linha: {}, Coluna: {}".format(
            self.tokens[self.actual].linha, self.tokens[self.actual].coluna))
        return False

    def termo(self):
        actual_index = self.actual
        if self.fator():
            notEnd = True
            while notEnd:
                notEnd = self.mult()
                if notEnd:
                    actual_index = self.actual
                    if not self.fator():
                        self.move_token_backward(actual_index)
                        notEnd = False
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de termo. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def mult(self):
        if self.match('*'):
            return True
        if self.match('/'):
            return True
        self.errors.append("Declaração inválida de operador (*,/). Linha: {}, Coluna: {}".format(
            self.tokens[self.actual].linha, self.tokens[self.actual].coluna))
        return False

    def fator(self):
        actual_index = self.actual
        if self.match('('):
            if self.expressao():
                if self.match(')'):
                    return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.var():
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.ativacao():
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.num():
            return True

        self.move_token_backward(actual_index)
        actual_index = self.actual
        if self.num_int():
            return True

        self.move_token_backward(actual_index)
        return False

    def ativacao(self):
        actual_index = self.actual
        if self.ident():
            if self.match('('):
                if self.args():
                    if self.match(')'):
                        return True

        self.move_token_backward(actual_index)
        return False

    # derivação opcional apenas
    def args(self):
        self.arg_lista()
        return True

    def arg_lista(self):
        actual_index = self.actual
        if self.expressao():
            notEnd = True
            while notEnd:
                notEnd = self.match(',')
                if notEnd:
                    actual_index = self.actual
                    if not self.expressao():
                        self.move_token_backward(actual_index)
                        notEnd = False
            return True

        self.move_token_backward(actual_index)
        return False

    def num(self):
        actual_index = self.actual
        self.soma()  # é opcional
        if self.num_int():
            if self.match('.'):
                if not self.num_int():
                    return False
            if self.match('E'):
                self.soma()  # é opcional
                if not self.num_int():
                    return False
            return True

        self.move_token_backward(actual_index)
        self.errors.append("Declaração inválida de número. Linha: {}, Coluna: {}".format(
            self.tokens[actual_index].linha, self.tokens[actual_index].coluna))
        return False

    def num_int(self):
        # É possível fazer o match aqui já que fornecemos o token INT
        return self.match('INT')

    def ident(self):
        return self.match('IDENTIFICADOR')

from lexical.lexeme import Lexemas


class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.actual = 0       # posição da lista de tokens
        self.success = False  # indicador da tradução correta
        self.errors = []      # faremos detecção de erros?

    def see_actual_token(self):
        return self.tokens[self.actual]

    def move_token_forward(self):
        self.actual += 1
        if self.actual == len(self.tokens):
            self.success = True

    def move_token_backward(self):
        self.actual -= 1

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
        self.programa()
        if self.success:
            print("success")

    def programa(self):
        self.declaracaoLista()

    def declaracaoLista(self):
        self.declaracao()
        while not self.success:
            if not self.declaracao():
                return False
        return True

    def declaracao(self):
        if self.var_declaracao():
            return True
        if self.fun_declaracao():
            return True

        return False

    def var_declaracao(self):
        if self.tipo_especificador():
            if self.ident():
                if self.match(';'):
                    return True

        if self.tipo_especificador():
            if self.ident():
                if self.match('['):
                    if self.num_int():
                        if self.match(']'):
                            while not self.success:
                                if not self.match('['):
                                    return False
                                if not self.num_int():
                                    return False
                                if not self.match(']'):
                                    return False
                            if self.match(';'):
                                return True
        return False

    def tipo_especificador(self):
        if self.match('int'):
            return True
        if self.match('float'):
            return True
        if self.match('char'):
            return True
        if self.match('void'):
            return True
        if self.match('struct'):
            if self.ident():
                if self.match('{'):
                    if self.atributos_declaracao():
                        if self.match('}'):
                            return True
        return False

    def atributos_declaracao(self):
        self.var_declaracao()
        while not self.success:
            if not self.var_declaracao():
                return False
        return True

    def fun_declaracao(self):
        if self.tipo_especificador():
            if self.ident():
                if self.match('('):
                    if self.params():
                        if self.match(')'):
                            if self.composto_decl():
                                return True
        return False

    def params(self):
        if self.param_lista():
            return True
        if self.match('void'):
            return True
        return False

    def param_lista(self):
        if self.param():
            while not self.success:
                if not self.match(','):
                    return False
                if not self.param():
                    return False
            return True
        return False

    # alterei a ordem das derivações da gramatica p/ rodar
    def param(self):
        if self.tipo_especificador():
            if self.ident():
                if self.match('['):
                    if self.match(']'):
                        return True
        if self.tipo_especificador():
            if self.ident():
                return True
        return False

    def composto_decl(self):
        if self.match('{'):
            if self.local_declaracoes():
                if self.comando_lista():
                    if self.match('}'):
                        return True
        return False

    def local_declaracoes(self):
        if self.match('{'):
            if self.var_declaracao():
                if self.match('}'):
                    return True
        return False

    def comando_lista(self):
        if self.match('{'):
            if self.comando():
                if self.match('}'):
                    return True
        return False

    def comando(self):
        if self.expressao_decl():
            return True
        if self.composto_decl():
            return True
        if self.selecao_decl():
            return True
        if self.iteracao_decl():
            return True
        if self.retorno_decl():
            return True
        return False

    def expressao_decl(self):
        if self.expressao():
            if self.match(';'):
                return True
        if self.match(';'):
            return True
        return False

    # alterei a ordem das derivações da gramatica p/ rodar
    def selecao_decl(self):
        if self.match('if'):
            if self.match('('):
                if self.expressao():
                    if self.match(')'):
                        if self.comando():
                            if self.match('else'):
                                if self.comando():
                                    return True
        if self.match('if'):
            if self.match('('):
                if self.expressao():
                    if self.match(')'):
                        if self.comando():
                            return True
        return False

    def iteracao_decl(self):
        if self.match('while'):
            if self.match('('):
                if self.expressao():
                    if self.match(')'):
                        if self.comando():
                            return True
        return False

    def retorno_decl(self):
        if self.match('return'):
            if self.match(';'):
                return True
        if self.match('return'):
            if self.expressao():
                if self.match(';'):
                    return True
        return False

    def expressao(self):
        if self.var():
            if self.match('='):
                if self.expressao():
                    return True
        if self.expressao_simples():
            return True
        return False

    # alterei a ordem das derivações da gramatica p/ rodar
    def var(self):
        if self.ident():
            if self.match('['):
                if self.expressao():
                    if self.match(']'):
                        while not self.success:
                            if not self.match('['):
                                return False
                            if not self.expressao():
                                return False
                            if not self.match(']'):
                                return False
                        return True
        if self.ident():
            return True
        return False

    def expressao_simples(self):
        if self.expressao_soma():
            if self.relacional():
                if self.expressao_soma():
                    return True
        if self.expressao_soma():
            return True
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
        return False

    def expressao_soma(self):
        if self.termo():
            while not self.success:
                if not self.soma():
                    return False
                if not self.termo():
                    return False
            return True
        return False

    def soma(self):
        if self.match('+'):
            return True
        if self.match('-'):
            return True
        return False

    def termo(self):
        if self.fator():
            while not self.success:
                if not self.mult():
                    return False
                if not self.fator():
                    return False
            return True
        return False

    def mult(self):
        if self.match('*'):
            return True
        if self.match('/'):
            return True
        return False

    def fator(self):
        if self.match('('):
            if self.expressao():
                if self.match(')'):
                    return True
        if self.var():
            return True
        if self.ativacao():
            return True
        if self.num():
            return True
        if self.num_int():
            return True
        return False

    def ativacao(self):
        if self.ident():
            if self.match('('):
                if self.args():
                    if self.match(')'):
                        return True
        return False

    # derivação opcional apenas
    def args(self):
        self.arg_lista()
        return True

    def arg_lista(self):
        if self.expressao():
            while not self.success:
                if not self.match(','):
                    return False
                if not self.expressao():
                    return False
            return True
        return False

    def num(self):
        self.soma()  # é opcional
        if self.digito():
            while self.digito():
                pass
            self.move_token_backward()
            if self.match('.'):
                if self.digito():
                    while self.digito():
                        pass
                    self.move_token_backward()
                else:
                    return False
            if self.match('E'):
                self.soma()  # é opcional
                if self.digito():
                    while self.digito():
                        pass
                    self.move_token_backward()
                else:
                    return False
            return True
        return False

    def num_int(self):
        if self.digito():
            while not self.success:
                if not self.digito():
                    return False
            return True
        return False

    def digito(self):
        # TODO:
        pass

    def ident(self):
        if self.letra():
            while not self.success:
                if (not self.letra()) and (not self.digito()):
                    return False
            return True
        return False

    def letra(self):
        # TODO:
        pass

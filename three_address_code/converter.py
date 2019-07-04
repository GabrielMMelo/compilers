from lexical.lexeme import Lexemas
from three_address_code.table import Table


class Conversor:
    def __init__(self, tokens, expressions, table_symbols):
        self.table = Table()
        self.tokens = tokens
        self.actual = 0       # posição da lista de tokens
        self.table_symbols = table_symbols
        self.expressions = expressions
        self.__verify_expressions()

    def __verify_expressions(self):
        remove = []
        for e in self.expressions:
            token = self.tokens[e]
            i = 1
            while token.tipo != Lexemas.lexema[';']:
                token = self.tokens[e + i]
                i += 1
            if i < 6:  # removendo as expreções com tamanho menor do que 5
                remove.append(e)
        for e in remove:
            self.expressions.remove(e)

    def convert(self):
        for e in self.expressions:
            identifier = self.tokens[e]  # guardando o identificador que o usuario utilizou
            e += 2  # para pular o identificador e =
            token = self.tokens[e]
            i = 1
            last_var = None
            name_temp = '_temp'
            pos = e
            while token.tipo != Lexemas.lexema[';']:
                if last_var:
                    arg1 = last_var
                    operator = token.tipo
                    arg2 = token.indiceTabelaSimbolo
                    pos += 2
                else:
                    arg1 = token.indiceTabelaSimbolo
                    operator = token.tipo
                    arg2 = token.indiceTabelaSimbolo
                    pos += 3

                result = name_temp + str(i)
                result = self.table_symbols.add(result)
                last_var = result
                self.table.insert(operator, arg1, arg2, result)

                token = self.tokens[pos]
                i += 1
            self.table.update_last(identifier.indiceTabelaSimbolo)
            self.table_symbols.remove_last()

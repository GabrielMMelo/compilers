from lexical.lexeme import Lexemas
from three_address_code.table import Table


class Conversor:
    def __init__(self, tokens, expressions, table_symbols):
        self.table = Table()
        self.tokens = tokens
        self.actual = 0  # posição da lista de tokens
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
            identifier = self.tokens[
                e]  # guardando o identificador que o usuario utilizou
            e += 2  # para pular o identificador e =
            token = self.tokens[e]
            i = 1
            last_var = None
            name_temp = '_temp'
            pos = e
            used = []
            while token.tipo != Lexemas.lexema[';']:
                pos_precedencia = self.__search(pos, used, '*', '/')
                print(' ')
                if pos_precedencia:
                    pos = pos_precedencia
                    arg1 = self.tokens[pos - 1].indiceTabelaSimbolo
                    operator = self.tokens[pos].tipo
                    arg2 = self.tokens[pos + 1].indiceTabelaSimbolo
                    used.append(pos)
                    pos = e  # retorna para inicio da expressão
                    precedencia = None

                elif pos in used:  # se um op de precedencia atualizar pos para outro op de precedencia
                    last_var = pos + 1
                    pos += 2
                    token = self.tokens[pos]
                    continue

                elif pos + 1 in used:  # se o proximo for um op de precedencia
                    last_var = pos + 2
                    pos += 3
                    token = self.tokens[pos]
                    continue

                elif last_var and pos != e:  # quando pos==e, desconsidera o last_var calculado pelo op de precedencia
                    arg1 = last_var
                    operator = token.tipo
                    arg2 = self.tokens[pos + 1].indiceTabelaSimbolo
                    pos += 2

                else:
                    arg1 = token.indiceTabelaSimbolo
                    operator = self.tokens[pos + 1].tipo
                    arg2 = self.tokens[pos + 2].indiceTabelaSimbolo
                    pos += 3

                result = name_temp + str(i)
                result = self.table_symbols.add(result)
                last_var = result
                self.table.insert(operator, arg1, arg2, result)

                token = self.tokens[pos]
                i += 1
            self.table.update_last(identifier.indiceTabelaSimbolo)
            self.table_symbols.remove_last()

    def __search(self, pos_atual, used, *operadores):
        busca = True
        while busca:
            if self.tokens[pos_atual].tipo in [
                    Lexemas.lexema[operador] for operador in operadores
            ] and pos_atual not in used:
                busca = False
                return pos_atual
            elif self.tokens[pos_atual].tipo == Lexemas.lexema[';']:
                busca = False
                return
            else:
                pos_atual += 1

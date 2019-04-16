import string
from lexical.token import Token
from lexical.lexeme import Lexemas
from lexical.symbol_table import TabelaSimbolos
from lexical.file_manager import GerenciarArquivo


class AnalisadorLexico:
    def __init__(self, arquivo):
        self.tabela_simbolos = TabelaSimbolos()
        self.arquivo = GerenciarArquivo(arquivo)
        self.tokens = []
        self.erros = []
        self.reservadas = ["int", "float", "struct", "if", "else", "while", "void", "return"]
        self.operadores = ["=", "<=", "<", ">", ">=", "==", "!=", "+", "-", "*", "/"]
        self.separadores = [",", ".", "[", "{", "(", ")", "}", "]", ";"]
        self.pular = ['\t', '\n', ' ']
        self.letras = "abcdefghijklmnopqrstuvwxyz"

    def e_reservada(self, palavra):
        if palavra in self.reservadas:
            return True
        return False

    def e_operador(self, palavra):
        if palavra in self.operadores:
            return True
        return False

    def e_separador(self, caracter):
        if caracter in self.separadores:
            return True
        return False

    def e_letra(self, caracter):
        if caracter in self.letras:
            return True
        return False

    def e_digito(self, caracter):
        if caracter in string.digits:
            return True
        return False

    def panic_mode(self, caracter_atual):
        try:
            while (caracter_atual not in self.pular) and (caracter_atual not in self.separadores):
                caracter_atual = self.arquivo.ler_caracter()
            self.arquivo.voltar_caracter()
        except UserWarning:
            # o panic mode chegpou no fim do arquivo
            # o erro será gerado após a chamada dessa funcao
            pass

    def analisar(self):
        try:
            while True:
                caracter_atual = self.arquivo.ler_caracter()
                linha = self.arquivo.get_linha()
                coluna = self.arquivo.get_coluna()
                cadeia = ''

                # identificador e palavra reservada
                if self.e_letra(caracter_atual):
                    cadeia += caracter_atual
                    erro = False
                    while caracter_atual != '\n':
                        caracter_atual = self.arquivo.ler_caracter()
                        if self.e_letra(caracter_atual) or self.e_digito(caracter_atual):
                            cadeia += caracter_atual
                        elif ((self.e_separador(caracter_atual) or caracter_atual == ' ' or caracter_atual == '\t')
                              or (self.e_operador(caracter_atual))):
                            self.arquivo.voltar_caracter()
                            break
                        elif caracter_atual != '\n':
                            self.panic_mode(caracter_atual)
                            self.erros.append("ERRO: identificador inválido. Linha: {}, Coluna: {}".
                                              format(linha, coluna))
                            erro = True
                            break

                    if not erro:
                        if self.e_reservada(cadeia):
                            self.tokens.append(Token("RESERVADA", cadeia, linha, coluna))
                        else:
                            id = self.tabela_simbolos.add(cadeia)
                            self.tokens.append(Token("IDENTIFICADOR", None, linha, coluna, id))

                # operadores
                elif self.e_operador(caracter_atual) or caracter_atual == "!":
                    caracter_seguinte = self.arquivo.ler_caracter()
                    juncao = caracter_atual + caracter_seguinte
                    if self.e_operador(juncao):
                        self.tokens.append(Token(Lexemas.lexema[juncao], juncao, linha, coluna))
                    else:
                        if caracter_atual == "!":
                            self.panic_mode(caracter_atual)
                            self.erros.append("ERRO: operador inválido. Linha: {}, Coluna: {}".format(linha, coluna))
                        else:
                            self.tokens.append(Token(Lexemas.lexema[caracter_atual], caracter_atual, linha, coluna))
                            self.arquivo.voltar_caracter()

                # constantes numéricas
                elif self.e_digito(caracter_atual):
                    float = False
                    erro = False
                    exponencial = False
                    while not caracter_atual == '\n':
                        if self.e_digito(caracter_atual):
                            cadeia += caracter_atual
                            caracter_atual = self.arquivo.ler_caracter()
                        elif caracter_atual == '.' and not float and not exponencial:  # para evitar que volte ao float
                            caracter_atual = self.arquivo.ler_caracter()
                            if self.e_digito(caracter_atual):
                                cadeia += '.'
                                float = True
                            else:
                                erro = True
                                break
                        elif caracter_atual == 'E' and not exponencial:
                            caracter_atual = self.arquivo.ler_caracter()
                            if self.e_digito(caracter_atual) or caracter_atual == '+' or caracter_atual == '-':
                                cadeia += 'E'
                                exponencial = True
                                if caracter_atual == '+' or caracter_atual == '-':
                                    linha_op = self.arquivo.get_linha()
                                    coluna_op = self.arquivo.get_coluna()
                                    self.tokens.append(Token(Lexemas.lexema[caracter_atual], caracter_atual, linha_op, coluna_op))
                            else:
                                erro = True
                                break
                        elif (((self.e_separador(caracter_atual) and caracter_atual != '.') or caracter_atual == ' '
                                or caracter_atual == '\t') or (self.e_operador(caracter_atual))):
                            self.arquivo.voltar_caracter()
                            break
                        elif not caracter_atual == '\n':
                            erro = True
                            break
                    if erro:
                        self.panic_mode(caracter_atual)
                        self.erros.append("ERRO: formato de constante numérica inválido. Linha: {}, Coluna: {}".
                                          format(linha, coluna))
                    elif float or exponencial:
                        id = self.tabela_simbolos.add(cadeia)
                        self.tokens.append(Token("FLOAT", None, linha, coluna, id))
                    else:
                        id = self.tabela_simbolos.add(cadeia)
                        self.tokens.append(Token("INT", None, linha, coluna, id))

                # separadores
                elif self.e_separador(caracter_atual):
                    self.tokens.append(Token(Lexemas.lexema[caracter_atual], caracter_atual, linha, coluna))

                elif caracter_atual not in self.pular:
                    self.panic_mode(caracter_atual)
                    self.erros.append("ERRO: caractere não suportado pela linguagem. Linha: {}, Coluna: {}".
                                          format(linha, coluna))

        except EOFError as e:
            self.erros.append(str(e))

        except UserWarning as e:
            pass  # final do arquivo

    def imprimir_tokens(self):
        print("\nTokens (<tipo, valor/id, linha, coluna>):")
        for t in self.tokens:
            print(t)

    def imprimir_tabela_simbolos(self):
        print("\nTabela de Simbolos:")
        print(self.tabela_simbolos)

    def imprimir_erros(self):
        if not self.erros:
            return
        print("Erros:")
        for e in self.erros:
            print(e)

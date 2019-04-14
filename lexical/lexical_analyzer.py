import string
from lexical.token_class import Token
from lexical.symbol_table import TabelaSimbolos
from lexical.file_manager import GerenciarArquivo


class AnalisadorLexico:
    def __init__(self):
        self.tabelaSimbolos = TabelaSimbolos()
        self.tokens = []
        self.erros = []
        self.reservadas = ["int", "float", "struct", "if", "else", "while", "void", "return"]
        self.operadoresRelacionais = ["=", "<=", "<", ">", ">=", "==", "!="]
        self.operadoresContas = ["+", "-", "*", "/"]
        self.separadores = [",", ".", "[", "{", "(", ")", "}", "]", ";"]
        self.pular = ['\t', '\n', ' ']
        self.letras = "abcdefghijklmnopqrstuvwxyz"

    def e_reservada(self, palavra):
        if palavra in self.reservadas:
            return True
        return False

    def e_operadorRelacional(self, palavra):
        if palavra in self.operadoresRelacionais:
            return True
        return False

    def e_operadorConta(self, palavra):
        if palavra in self.operadoresContas:
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

    def analisador(self, arquivo):
        arquivo = GerenciarArquivo(arquivo)

        try:
            while True:
                caracter_atual = arquivo.ler_caracter()
                print("Lido: ", caracter_atual)
        except EOFError as e:
            self.erros.append(str(e))
            # remover futuramente esses prints de debug
            print('erro comentario')
            print(self.erros)
        except UserWarning as e:
            # acabou o arquivo
            # remover futuramente esse print de debug
            print(str(e))

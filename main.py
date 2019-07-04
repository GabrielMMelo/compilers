import sys
import os
from lexical.analyzer import AnalisadorLexico
from syntactic.analyzer import AnalisadorSintatico
from three_address_code.converter import Conversor


if __name__ == "__main__":
    arquivo = ""
    if len(sys.argv) == 2:
        arquivo = sys.argv[1]
        existe = os.path.isfile(arquivo)
        if not existe:
            print("O arquivo de entrada não existe ou não foi encontrado.")
            sys.exit()
    else:
        print("Número inválido de argumentos. Informe o arquivo de entrada")
        sys.exit()

    lexico = AnalisadorLexico(arquivo)
    resultado_lexico = lexico.analisar()
    # lexico.imprimir_tokens()
    # print(lexico.tabela_simbolos)
    # lexico.imprimir_erros()

    if resultado_lexico:
        sintatico = AnalisadorSintatico(lexico.tokens)
        if sintatico.analisar():
            # print("Sucesso!")
            three_adress_code = Conversor(lexico.tokens, sintatico.expressions, lexico.tabela_simbolos)
            three_adress_code.convert()
            print(three_adress_code.table_symbols)
            print(three_adress_code.table)
        else:
            print("Erro(s) sintático!")
            sintatico.imprimir_erros()
    else:
        print("Erro(s) léxico!")
        lexico.imprimir_erros()

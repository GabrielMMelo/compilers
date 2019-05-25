import sys
import os
from lexical.analyzer import AnalisadorLexico
from syntactic.analyzer import AnalisadorSintatico


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
    lexico.analisar()
    # lexico.imprimir_tokens()
    # lexico.imprimir_tabela_simbolos()
    # lexico.imprimir_erros()

    sintatico = AnalisadorSintatico(lexico.tokens)
    sintatico.analisar()

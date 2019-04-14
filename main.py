import sys
import os
from lexical.lexical_analyzer import AnalisadorLexico


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

    analisador = AnalisadorLexico(arquivo)
    analisador.analisar()
    analisador.imprimir_tokens()
    analisador.imprimir_tabela_simbolos()
    analisador.imprimir_erros()



class GerenciarArquivo:

    def __init__(self, arquivo):
        self.arquivo = open(arquivo, "r")
        self.linha = 1
        self.coluna = 1
        self.indice = 0
        self.linha_entrada = self.arquivo.readline()
        self.tamanho_linha = len(self.linha_entrada)

    def __ler_caracter_aux(self):
        if self.indice == self.tamanho_linha:
            self.linha_entrada = self.arquivo.readline()
            if self.linha_entrada:
                self.tamanho_linha = len(self.linha_entrada)
                self.linha += 1
                self.coluna = 1
                self.indice = 0
                return self.__ler_caracter_aux()
            else:
                raise UserWarning("Fim de arquivo")
        else:
            self.indice += 1
            self.coluna += 1
            return self.linha_entrada[self.indice - 1]

    def __ler_e_pular_comentario(self):
        caracter_atual = self.__ler_caracter_aux()
        
        if caracter_atual == "/":
            caracter_seguinte = self.__ler_caracter_aux()
            if caracter_seguinte == "*":
                coluna_inicio_comentario = self.coluna - 2
                linha_inicio_comentario = self.linha
                try:
                    caracter_atual = self.__ler_caracter_aux()
                    nao_acabou_comentario = True

                    while nao_acabou_comentario:
                        while caracter_atual != "*":
                            caracter_atual = self.__ler_caracter_aux()
                        caracter_seguinte = self.__ler_caracter_aux()
                        if caracter_seguinte == "/":
                            nao_acabou_comentario = False
                            caracter_atual = self.__ler_caracter_aux()
                        else:
                            caracter_atual = caracter_seguinte
                except UserWarning:
                    raise EOFError("ERRO: Comentário não fechado! Linha: {}, Coluna: {}".format(linha_inicio_comentario, coluna_inicio_comentario))
            else:
                self.coluna -= 1
                self.indice -= 1

        return caracter_atual

    def ler_caracter(self):
        return self.__ler_e_pular_comentario()

    def get_linha(self):
        return self.linha

    def get_coluna(self):
        return self.coluna

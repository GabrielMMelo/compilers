class Table:
    """
    Tabela para o armazenamento da geração de código de três endereços
    a abordagem utilizada é a de quádrupla
    """
    def __init__(self):
        self.__table = []

    def insert(self, operator, arg1, agr2, result):
        '''
        Insere uma nova entrada na tabela

        :param operator: operador aritmético (iremos guardar o lexema?)
        :param arg1: variável da esquerada (iremos guardar a posição da tabela de símbolos?)
        :param agr2: variável da direita (iremos guardar a posição da tabela de símbolos?)
        :param result: variável que guarda o resultado da operação (iremos guardar a posição da tabela de símbolos?)
        '''
        self.__table.append([operator, arg1, agr2, result])

    def __str__(self):
        string = ""
        for index, line in enumerate(self.__table, 1):
            string += "{} -> {}, {}, {}, {}".format(index, line[0], line[1], line[2], line[3])
        return string

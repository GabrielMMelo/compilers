from enum import Enum, auto


class Lexemas(Enum):
    IDENTIFICADOR = auto()

    INT    = auto()
    FLOAT  = auto()
    STRUCT = auto()
    IF     = auto()
    ELSE   = auto()
    WHILE  = auto()
    VOID   = auto()
    RETURN = auto()

    OP_ATRIBUICAO  = auto()
    OP_IGUAL       = auto()
    OP_MAIOR       = auto()
    OP_MENOR       = auto()
    OP_MAIOR_IGUAL = auto()
    OP_MENOR_IGUAL = auto()
    OP_DIFERENTE   = auto()

    OP_SOMA          = auto()
    OP_SUBTRACAO     = auto()
    OP_MULTIPLICACAO = auto()
    OP_DIVISAO       = auto()

    SEP_PONTO           = auto()
    SEP_PONTO_VIRGULA   = auto()
    SEP_ABRE_PARENTESE  = auto()
    SEP_FECHA_PARENTESE = auto()
    SEP_ABRE_CHAVE      = auto()
    SEP_FECHA_CHAVE     = auto()
    SEP_ABRE_COLCHETE   = auto()
    SEP_FECHA_COLCHETE  = auto()

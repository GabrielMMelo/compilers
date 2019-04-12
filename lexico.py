class AnalisadorLexico:
    def __init__(self):
	    # int, float, struct, if, else, while, void, return palavras reservadas
		self.reservadas = [ "int", "float", "struct","if", "else", "while", "void","return","char"]
		#<relacional>::=<=|<|>|>=|==|!=
        self.operadoresRelacionais = ["=","<=","<", ">","==", "!="]
        #<soma>::=+|- 
        #<mult>::=*|/
        self.operadoresContas = ["+","-","*","/"]
        #separadores  
        #{,},[,],(,),;, . '      
		self.separadores = [".", "[", "{", "(", ")", "}", "]", ";"]
		self.simbolos = ''' ! '' () *+,-./0123456789;<=>[]abcdefghijklmnopqrstuvxwyz}{'''
        	def e_reservada(self, palavra):
		if palavra in self.reservadas:
			return True
		return False

        def e_operadorRelacional(self, palavra):
            if palavra in self.operadoresRelacionais:
                return True
            return False
        def e_operadorConta(self, palavra):
            if palavra in self.operadoresConta:
                return True
            return False
        def e_separador(self, caracter):
            if caracter in self.separadores:
                return True
            return False

        def e_letra(self, caracter):
            if caracter in string.ascii_letters or caracter in "_":
                return True
            return False

        def e_digito(self, caracter):
            if caracter in string.digits:
                return True
            return False

        def e_simbolo(self, caracter):
            if caracter in self.simbolos:
                return True
            return False

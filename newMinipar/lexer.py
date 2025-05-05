"""
lexer.py - Analisador Léxico para a linguagem MiniPar
Responsável pela análise léxica do código fonte escrito na linguagem MiniPar
"""

class Token:
    """
    Classe que representa um token identificado durante a análise léxica
    """
    # Tipos de tokens
    # Palavras-chave
    PROGRAMA = "PROGRAMA"
    SEQ = "SEQ"
    PAR = "PAR"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    BOOL = "BOOL"
    INT = "INT"
    STRING = "STRING"
    C_CHANNEL = "C_CHANNEL"
    SEND = "SEND"
    RECEIVE = "RECEIVE"
    DEF = "DEF"
    RETURN = "RETURN"
    OUTPUT = "OUTPUT"     # Palavra-chave para saída (equivalente ao print)
    INPUT = "INPUT"       # Palavra-chave para entrada
    
    # Operadores
    IGUAL = "IGUAL"           # =
    MAIS = "MAIS"             # +
    MENOS = "MENOS"           # -
    MULT = "MULT"             # *
    DIV = "DIV"               # /
    MAIOR = "MAIOR"           # >
    MENOR = "MENOR"           # <
    MAIOR_IGUAL = "MAIOR_IGUAL"  # >=
    MENOR_IGUAL = "MENOR_IGUAL"  # <=
    IGUAL_IGUAL = "IGUAL_IGUAL"  # ==
    DIFERENTE = "DIFERENTE"      # !=
    AND = "AND"               # and
    OR = "OR"                 # or
    NOT = "NOT"               # not
    
    # Outros símbolos
    ABRE_PAREN = "ABRE_PAREN"    # (
    FECHA_PAREN = "FECHA_PAREN"  # )
    ABRE_CHAVES = "ABRE_CHAVES"  # {
    FECHA_CHAVES = "FECHA_CHAVES"  # }
    ABRE_COLCHETES = "ABRE_COLCHETES"  # [
    FECHA_COLCHETES = "FECHA_COLCHETES"  # ]
    VIRGULA = "VIRGULA"       # ,
    PONTO = "PONTO"           # .
    PONTO_VIRGULA = "PONTO_VIRGULA"  # ;
    DOIS_PONTOS = "DOIS_PONTOS"  # :
    
    # Tipos de dados
    ID = "ID"                 # Identificadores
    INT_CONST = "INT_CONST"   # Constantes inteiras
    FLOAT_CONST = "FLOAT_CONST"  # Constantes de ponto flutuante
    STRING_CONST = "STRING_CONST"  # Constantes de string
    TRUE = "TRUE"             # true
    FALSE = "FALSE"           # false
    
    # EOF
    EOF = "EOF"               # Fim do arquivo
    
    def __init__(self, tipo, valor=None, linha=0, coluna=0):
        """
        Inicializa um novo token
        :param tipo: O tipo do token (conforme as constantes de classe)
        :param valor: O valor associado ao token (para identificadores, constantes, etc.)
        :param linha: A linha onde o token foi encontrado
        :param coluna: A coluna onde o token foi encontrado
        """
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna
    
    def __str__(self):
        """
        Retorna uma representação em string do token
        """
        if self.valor is not None:
            return f"Token({self.tipo}, {self.valor}, linha={self.linha}, coluna={self.coluna})"
        else:
            return f"Token({self.tipo}, linha={self.linha}, coluna={self.coluna})"
    
    def __repr__(self):
        return self.__str__()


class MiniParLexer:
    """
    Analisador léxico para a linguagem MiniPar
    Converte o código fonte em uma sequência de tokens
    """
    
    # Palavras-chave da linguagem
    PALAVRAS_CHAVE = {
        "programa-minipar": Token.PROGRAMA,
        "programa_minipar": Token.PROGRAMA,
        "SEQ": Token.SEQ,
        "PAR": Token.PAR,
        "if": Token.IF,
        "else": Token.ELSE,
        "while": Token.WHILE,
        "bool": Token.BOOL,
        "int": Token.INT,
        "string": Token.STRING,
        "c_channel": Token.C_CHANNEL,
        "send": Token.SEND,
        "receive": Token.RECEIVE,
        "def": Token.DEF,
        "return": Token.RETURN,
        "and": Token.AND,
        "or": Token.OR,
        "not": Token.NOT,
        "True": Token.TRUE,
        "False": Token.FALSE,
        "output": Token.OUTPUT,  # Adicionado para saída
        "input": Token.INPUT     # Adicionado para entrada
    }
    
    def __init__(self, codigo_fonte):
        """
        Inicializa o analisador léxico com o código fonte
        :param codigo_fonte: O código fonte a ser analisado
        """
        self.codigo_fonte = codigo_fonte
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        self.tamanho = len(codigo_fonte)
        self.tokens = []
        
    def char_atual(self):
        """
        Retorna o caractere atual na posição
        """
        if self.posicao >= self.tamanho:
            return None
        return self.codigo_fonte[self.posicao]
    
    def proximo_char(self):
        """
        Avança para o próximo caractere e o retorna
        """
        char = self.char_atual()
        self.avancar()
        return char
    
    def espiar_proximo(self):
        """
        Retorna o próximo caractere sem avançar a posição
        """
        pos = self.posicao + 1
        if pos >= self.tamanho:
            return None
        return self.codigo_fonte[pos]
    
    def avancar(self):
        """
        Avança a posição atual no código fonte
        """
        if self.char_atual() == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        self.posicao += 1
    
    def pular_espacos_em_branco(self):
        """
        Avança a posição pulando espaços em branco, tabs e quebras de linha
        """
        while self.char_atual() is not None and self.char_atual().isspace():
            self.avancar()
    
    def pular_comentarios(self):
        """
        Pula comentários na forma # até o final da linha
        """
        if self.char_atual() == '#':
            while self.char_atual() is not None and self.char_atual() != '\n':
                self.avancar()
    
    def identificar_numero(self):
        """
        Identifica e retorna um token para um número (inteiro ou float)
        """
        inicio_coluna = self.coluna
        valor = ""
        tem_ponto = False
        
        while self.char_atual() is not None and (self.char_atual().isdigit() or self.char_atual() == '.'):
            if self.char_atual() == '.':
                if tem_ponto:  # Já tem um ponto, erro
                    raise Exception(f"Número mal formado na linha {self.linha}, coluna {self.coluna}")
                tem_ponto = True
            valor += self.char_atual()
            self.avancar()
        
        if tem_ponto:
            return Token(Token.FLOAT_CONST, float(valor), self.linha, inicio_coluna)
        else:
            return Token(Token.INT_CONST, int(valor), self.linha, inicio_coluna)
    
    def identificar_identificador_ou_palavra_chave(self):
        """
        Identifica e retorna um token para um identificador ou palavra-chave
        """
        inicio_coluna = self.coluna
        valor = ""
        
        # Identificadores começam com letra ou underscore
        if self.char_atual().isalpha() or self.char_atual() == '_':
            valor += self.char_atual()
            self.avancar()
            
            # Identificadores podem conter letras, números ou underscore
            while self.char_atual() is not None and (self.char_atual().isalnum() or self.char_atual() == '_' or self.char_atual() == '-'):
                valor += self.char_atual()
                self.avancar()
            
            # Verifica se é uma palavra-chave
            tipo_token = self.PALAVRAS_CHAVE.get(valor, Token.ID)  # Converter para minúsculo para case insensitivity
            return Token(tipo_token, valor, self.linha, inicio_coluna)
        
        return None
    
    def identificar_string(self):
        """
        Identifica e retorna um token para uma string entre aspas
        """
        inicio_coluna = self.coluna
        delimitador = self.char_atual()  # " ou '
        self.avancar()  # Pula o primeiro delimitador
        
        valor = ""
        while self.char_atual() is not None and self.char_atual() != delimitador:
            if self.char_atual() == '\\':  # Caractere de escape
                self.avancar()
                if self.char_atual() == 'n':
                    valor += '\n'
                elif self.char_atual() == 't':
                    valor += '\t'
                elif self.char_atual() == '\\':
                    valor += '\\'
                elif self.char_atual() == delimitador:
                    valor += delimitador
                else:
                    valor += '\\' + self.char_atual()
            else:
                valor += self.char_atual()
            self.avancar()
        
        if self.char_atual() is None:
            raise Exception(f"String não fechada na linha {self.linha}")
        
        self.avancar()  # Pula o segundo delimitador
        return Token(Token.STRING_CONST, valor, self.linha, inicio_coluna)
    
    def obter_proximo_token(self):
        """
        Identifica e retorna o próximo token do código fonte
        """
        # Pula espaços em branco e comentários
        self.pular_espacos_em_branco()
        while self.char_atual() == '#':
            self.pular_comentarios()
            self.pular_espacos_em_branco()
        
        # Fim do arquivo
        if self.char_atual() is None:
            return Token(Token.EOF, None, self.linha, self.coluna)
        
        # Caractere atual
        char = self.char_atual()
        
        # Identificadores e palavras-chave
        if char.isalpha() or char == '_':
            return self.identificar_identificador_ou_palavra_chave()
        
        # Números
        if char.isdigit():
            return self.identificar_numero()
        
        # Strings
        if char == '"' or char == "'":
            return self.identificar_string()
        
        # Operadores e símbolos
        inicio_coluna = self.coluna
        if char == '=':
            self.avancar()
            if self.char_atual() == '=':
                self.avancar()
                return Token(Token.IGUAL_IGUAL, "==", self.linha, inicio_coluna)
            return Token(Token.IGUAL, "=", self.linha, inicio_coluna)
        
        elif char == '+':
            self.avancar()
            return Token(Token.MAIS, "+", self.linha, inicio_coluna)
        
        elif char == '-':
            self.avancar()
            return Token(Token.MENOS, "-", self.linha, inicio_coluna)
        
        elif char == '*':
            self.avancar()
            return Token(Token.MULT, "*", self.linha, inicio_coluna)
        
        elif char == '/':
            self.avancar()
            return Token(Token.DIV, "/", self.linha, inicio_coluna)
        
        elif char == '>':
            self.avancar()
            if self.char_atual() == '=':
                self.avancar()
                return Token(Token.MAIOR_IGUAL, ">=", self.linha, inicio_coluna)
            return Token(Token.MAIOR, ">", self.linha, inicio_coluna)
        
        elif char == '<':
            self.avancar()
            if self.char_atual() == '=':
                self.avancar()
                return Token(Token.MENOR_IGUAL, "<=", self.linha, inicio_coluna)
            return Token(Token.MENOR, "<", self.linha, inicio_coluna)
        
        elif char == '!':
            self.avancar()
            if self.char_atual() == '=':
                self.avancar()
                return Token(Token.DIFERENTE, "!=", self.linha, inicio_coluna)
            return Token(Token.NOT, "!", self.linha, inicio_coluna)
        
        elif char == '(':
            self.avancar()
            return Token(Token.ABRE_PAREN, "(", self.linha, inicio_coluna)
        
        elif char == ')':
            self.avancar()
            return Token(Token.FECHA_PAREN, ")", self.linha, inicio_coluna)
        
        elif char == '{':
            self.avancar()
            return Token(Token.ABRE_CHAVES, "{", self.linha, inicio_coluna)
        
        elif char == '}':
            self.avancar()
            return Token(Token.FECHA_CHAVES, "}", self.linha, inicio_coluna)
        
        elif char == '[':
            self.avancar()
            return Token(Token.ABRE_COLCHETES, "[", self.linha, inicio_coluna)
        
        elif char == ']':
            self.avancar()
            return Token(Token.FECHA_COLCHETES, "]", self.linha, inicio_coluna)
        
        elif char == ',':
            self.avancar()
            return Token(Token.VIRGULA, ",", self.linha, inicio_coluna)
        
        elif char == '.':
            self.avancar()
            return Token(Token.PONTO, ".", self.linha, inicio_coluna)
        
        elif char == ';':
            self.avancar()
            return Token(Token.PONTO_VIRGULA, ";", self.linha, inicio_coluna)
        
        elif char == ':':
            self.avancar()
            return Token(Token.DOIS_PONTOS, ":", self.linha, inicio_coluna)
        
        # Caractere não reconhecido
        raise Exception(f"Caractere não reconhecido: '{char}' na linha {self.linha}, coluna {self.coluna}")
    
    def tokenizar(self):
        """
        Converte todo o código fonte em uma lista de tokens
        """
        tokens = []
        while True:
            token = self.obter_proximo_token()
            tokens.append(token)
            if token.tipo == Token.EOF:
                break
        return tokens


# Função para testar o analisador léxico com um exemplo simples
def testar_lexer(codigo_fonte):
    """
    Testa o analisador léxico com um código fonte
    :param codigo_fonte: O código fonte a ser analisado
    """
    lexer = MiniParLexer(codigo_fonte)
    tokens = lexer.tokenizar()
    for token in tokens:
        print(token)


# Exemplo de código para teste (um trecho do Programa de Teste 1)
if __name__ == "__main__":
    codigo_teste = """
    programa-miniPar
    # Programa cliente servidor de uma calculadora aritmética simples
    c_channel calculadora computador_1 computador_2
    
    SEQ
        # Operações da calculadora
        operacao = "+"
        valor1 = 10
        valor2 = 20
        resultado = valor1 + valor2
        calculadora.send(operacao, valor1, valor2, resultado)
        output resultado
        # Recebendo o resultado
    """
    
    print("Testando o analisador léxico:")
    testar_lexer(codigo_teste)
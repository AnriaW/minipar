"""
parser.py - Analisador Sintático para a linguagem MiniPar
Responsável pela análise sintática do código fonte escrito na linguagem MiniPar
"""

from lexer import Token, MiniParLexer

class NoBlocoSEQ:
    def __init__(self, stmts):
        self.stmts = stmts
    
    def __str__(self):
        return f"BlocoSEQ({self.stmts})"

class NoBlocoPAR:
    def __init__(self, stmts):
        self.stmts = stmts
    
    def __str__(self):
        return f"BlocoPAR({self.stmts})"

class NoDeclaracaoCanal:
    def __init__(self, nome, comp1, comp2):
        self.nome = nome
        self.comp1 = comp1
        self.comp2 = comp2
    
    def __str__(self):
        return f"DeclaracaoCanal({self.nome}, {self.comp1}, {self.comp2})"

class NoEnvio:
    def __init__(self, canal, args):
        self.canal = canal
        self.args = args
    
    def __str__(self):
        return f"Envio({self.canal}, {self.args})"

class NoRecepcao:
    def __init__(self, canal, args):
        self.canal = canal
        self.args = args
    
    def __str__(self):
        return f"Recepcao({self.canal}, {self.args})"

class NoAtribuicao:
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
    
    def __str__(self):
        return f"Atribuicao({self.id}, {self.expr})"

class NoExpressao:
    def __init__(self, esquerda, operador=None, direita=None):
        self.esquerda = esquerda
        self.operador = operador
        self.direita = direita
    
    def __str__(self):
        if self.operador:
            return f"Expressao({self.esquerda} {self.operador} {self.direita})"
        return f"Expressao({self.esquerda})"

class NoValor:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
    
    def __str__(self):
        return f"Valor({self.tipo}, {self.valor})"

class NoCondicional:
    def __init__(self, condicao, bloco_verdadeiro, bloco_falso=None):
        self.condicao = condicao
        self.bloco_verdadeiro = bloco_verdadeiro
        self.bloco_falso = bloco_falso
    
    def __str__(self):
        if self.bloco_falso:
            return f"If({self.condicao}, {self.bloco_verdadeiro}, {self.bloco_falso})"
        return f"If({self.condicao}, {self.bloco_verdadeiro})"

class NoEnquanto:
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco
    
    def __str__(self):
        return f"While({self.condicao}, {self.bloco})"

class NoSaida:
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return f"Output({self.expr})"

class NoEntrada:
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return f"Input({self.id})"

class NoFuncao:
    def __init__(self, nome, parametros, corpo):
        self.nome = nome
        self.parametros = parametros
        self.corpo = corpo
    
    def __str__(self):
        return f"Funcao({self.nome}, {self.parametros}, {self.corpo})"

class NoChamadaFuncao:
    def __init__(self, nome, argumentos):
        self.nome = nome
        self.argumentos = argumentos
    
    def __str__(self):
        return f"ChamadaFuncao({self.nome}, {self.argumentos})"

class NoRetorno:
    def __init__(self, expr=None):
        self.expr = expr
    
    def __str__(self):
        if self.expr:
            return f"Retorno({self.expr})"
        return "Retorno()"

class NoDeclaracaoVariavel:
    def __init__(self, tipo, id, valor=None):
        self.tipo = tipo
        self.id = id
        self.valor = valor
    
    def __str__(self):
        if self.valor:
            return f"DeclaracaoVar({self.tipo}, {self.id}, {self.valor})"
        return f"DeclaracaoVar({self.tipo}, {self.id})"

class NoPrograma:
    def __init__(self, bloco):
        self.bloco = bloco
    
    def __str__(self):
        return f"Programa({self.bloco})"


class MiniParParser:
    """
    Analisador sintático para a linguagem MiniPar
    Verifica se a estrutura do programa está de acordo com a gramática da linguagem
    """
    
    def __init__(self, lexer):
        """
        Inicializa o analisador sintático com o analisador léxico
        :param lexer: O analisador léxico que fornecerá os tokens
        """
        self.lexer = lexer
        self.tokens = lexer.tokenizar()
        self.pos_atual = 0
        self.token_atual = self.tokens[0]
    
    def erro(self, mensagem):
        """
        Gera uma mensagem de erro sintático
        :param mensagem: A mensagem de erro
        """
        linha = self.token_atual.linha
        coluna = self.token_atual.coluna
        raise Exception(f"Erro sintático na linha {linha}, coluna {coluna}: {mensagem}")
    
    def avancar(self):
        """
        Avança para o próximo token
        """
        self.pos_atual += 1
        if self.pos_atual < len(self.tokens):
            self.token_atual = self.tokens[self.pos_atual]
        return self.token_atual
    
    def verificar_tipo(self, tipo):
        """
        Verifica se o token atual é do tipo esperado
        :param tipo: O tipo esperado do token
        :return: True se for do tipo esperado, False caso contrário
        """
        return self.token_atual.tipo == tipo
    
    def consumir(self, tipo, mensagem):
        """
        Consome um token se for do tipo esperado, caso contrário gera um erro
        :param tipo: O tipo esperado do token
        :param mensagem: A mensagem de erro caso o token não seja do tipo esperado
        :return: O token consumido
        """
        if self.verificar_tipo(tipo):
            token = self.token_atual
            self.avancar()
            return token
        self.erro(mensagem)
    
    def parsear(self):
        """
        Inicia o processo de análise sintática do programa
        :return: A árvore sintática abstrata (AST) do programa
        """
        programa = self.programa()
        if not self.verificar_tipo(Token.EOF):
            self.erro("Esperado fim do arquivo após o programa")
        return programa
    
    def programa(self):
        """
        programa_minipar -> bloco_stmt
        :return: Um nó NoPrograma representando o programa
        """
        # Verificar se o programa começa com a palavra-chave "programa-minipar" ou "programa_minipar"
        if self.verificar_tipo(Token.PROGRAMA):
            self.avancar()
        else:
            self.erro("Esperado 'programa-minipar' ou 'programa_minipar' no início do programa")
        
        # Analisar o bloco principal do programa
        bloco = self.bloco_stmt()
        
        return NoPrograma(bloco)
    
    def bloco_stmt(self):
        """
        bloco_stmt -> bloco_SEQ | bloco_PAR
        :return: Um nó NoBlocoSEQ ou NoBlocoPAR representando o bloco
        """
        if self.verificar_tipo(Token.SEQ):
            return self.bloco_SEQ()
        elif self.verificar_tipo(Token.PAR):
            return self.bloco_PAR()
        else:
            self.erro("Esperado 'SEQ' ou 'PAR' para iniciar um bloco")
    
    def bloco_SEQ(self):
        """
        bloco_SEQ -> SEQ stmts
        :return: Um nó NoBlocoSEQ representando o bloco sequencial
        """
        self.consumir(Token.SEQ, "Esperado 'SEQ'")
        stmts = self.stmts()
        return NoBlocoSEQ(stmts)
    
    def bloco_PAR(self):
        """
        bloco_PAR -> PAR stmts
        :return: Um nó NoBlocoPAR representando o bloco paralelo
        """
        self.consumir(Token.PAR, "Esperado 'PAR'")
        stmts = self.stmts()
        return NoBlocoPAR(stmts)
    
    def stmts(self):
        """
        stmts -> stmt stmts | vazio
        :return: Uma lista de nós representando as instruções
        """
        statements = []
        
        # Continua analisando instruções até encontrar um token que não inicia uma instrução
        while not self.verificar_tipo(Token.EOF) and not self.final_de_bloco():
            stmt = self.stmt()
            statements.append(stmt)
        
        return statements
    
    def final_de_bloco(self):
        """
        Verifica se o token atual indica o final de um bloco
        :return: True se for o final de um bloco, False caso contrário
        """
        # Na linguagem MiniPar, os blocos são indentados e não há marcadores explícitos de fim de bloco
        # Consideramos o final de um bloco quando encontramos um token que não pode iniciar uma instrução
        # ou quando encontramos outro bloco SEQ ou PAR
        return (self.verificar_tipo(Token.SEQ) or 
                self.verificar_tipo(Token.PAR) or 
                self.verificar_tipo(Token.ELSE))
    
    def stmt(self):
        """
        stmt -> atribuicao | declaracao_canal | envio | recepcao | if_stmt | while_stmt | output_stmt | input_stmt | funcao_def | chamada_funcao | retorno
        :return: Um nó representando a instrução
        """
        if self.verificar_tipo(Token.C_CHANNEL):
            return self.declaracao_canal()
        elif self.verificar_tipo(Token.IF):
            return self.if_stmt()
        elif self.verificar_tipo(Token.WHILE):
            return self.while_stmt()
        elif self.verificar_tipo(Token.OUTPUT):
            return self.output_stmt()
        elif self.verificar_tipo(Token.INPUT):
            return self.input_stmt()
        elif self.verificar_tipo(Token.DEF):
            return self.funcao_def()
        elif self.verificar_tipo(Token.RETURN):
            return self.retorno()
        elif self.verificar_tipo(Token.BOOL) or self.verificar_tipo(Token.INT) or self.verificar_tipo(Token.STRING):
            return self.declaracao_variavel()
        elif self.verificar_tipo(Token.ID):
            # Pode ser atribuição, envio, recepção ou chamada de função
            token = self.token_atual
            self.avancar()
            
            if self.verificar_tipo(Token.IGUAL):
                # Atribuição: id = expr
                self.avancar()
                expr = self.expr()
                return NoAtribuicao(token.valor, expr)
            elif self.verificar_tipo(Token.PONTO):
                # Operação de canal: canal.send(...) ou canal.receive(...)
                self.avancar()
                if self.verificar_tipo(Token.SEND):
                    self.avancar()
                    args = self.argumentos()
                    return NoEnvio(token.valor, args)
                elif self.verificar_tipo(Token.RECEIVE):
                    self.avancar()
                    args = self.argumentos()
                    return NoRecepcao(token.valor, args)
                else:
                    self.erro("Esperado 'send' ou 'receive' após '.'")
            elif self.verificar_tipo(Token.ABRE_PAREN):
                # Chamada de função: id(args)
                args = self.argumentos()
                return NoChamadaFuncao(token.valor, args)
            else:
                self.erro("Esperado '=', '.', ou '(' após identificador")
        else:
            self.erro("Erro de sintaxe: instrução inválida")
    
    def declaracao_canal(self):
        """
        declaracao_canal -> c_channel id id id
        :return: Um nó NoDeclaracaoCanal representando a declaração de canal
        """
        self.consumir(Token.C_CHANNEL, "Esperado 'c_channel'")
        nome = self.consumir(Token.ID, "Esperado identificador para o nome do canal").valor
        comp1 = self.consumir(Token.ID, "Esperado identificador para o primeiro computador").valor
        comp2 = self.consumir(Token.ID, "Esperado identificador para o segundo computador").valor
        return NoDeclaracaoCanal(nome, comp1, comp2)
    
    def if_stmt(self):
        """
        if_stmt -> if ( bool ) stmt [else stmt]
        :return: Um nó NoCondicional representando a estrutura condicional
        """
        self.consumir(Token.IF, "Esperado 'if'")
        self.consumir(Token.ABRE_PAREN, "Esperado '(' após 'if'")
        condicao = self.bool_expr()
        self.consumir(Token.FECHA_PAREN, "Esperado ')' após a condição")
        
        bloco_verdadeiro = self.stmt()
        
        bloco_falso = None
        if self.verificar_tipo(Token.ELSE):
            self.avancar()
            bloco_falso = self.stmt()
        
        return NoCondicional(condicao, bloco_verdadeiro, bloco_falso)
    
    def while_stmt(self):
        """
        while_stmt -> while ( bool ) stmt
        :return: Um nó NoEnquanto representando a estrutura de repetição
        """
        self.consumir(Token.WHILE, "Esperado 'while'")
        self.consumir(Token.ABRE_PAREN, "Esperado '(' após 'while'")
        condicao = self.bool_expr()
        self.consumir(Token.FECHA_PAREN, "Esperado ')' após a condição")
        
        bloco = self.stmt()
        
        return NoEnquanto(condicao, bloco)
    
    def output_stmt(self):
        """
        output_stmt -> output expr
        :return: Um nó NoSaida representando a instrução de saída
        """
        self.consumir(Token.OUTPUT, "Esperado 'output'")
        expr = self.expr()
        return NoSaida(expr)
    
    def input_stmt(self):
        """
        input_stmt -> input id
        :return: Um nó NoEntrada representando a instrução de entrada
        """
        self.consumir(Token.INPUT, "Esperado 'input'")
        id = self.consumir(Token.ID, "Esperado identificador após 'input'").valor
        return NoEntrada(id)
    
    def funcao_def(self):
        """
        funcao_def -> def id ( parametros ) : stmt
        :return: Um nó NoFuncao representando a definição de função
        """
        self.consumir(Token.DEF, "Esperado 'def'")
        nome = self.consumir(Token.ID, "Esperado identificador para o nome da função").valor
        
        self.consumir(Token.ABRE_PAREN, "Esperado '(' após o nome da função")
        parametros = self.parametros()
        self.consumir(Token.FECHA_PAREN, "Esperado ')' após os parâmetros")
        
        self.consumir(Token.DOIS_PONTOS, "Esperado ':' após os parâmetros da função")
        
        corpo = self.stmt()
        
        return NoFuncao(nome, parametros, corpo)
    
    def parametros(self):
        """
        parametros -> id [, id]*
        :return: Uma lista de strings representando os parâmetros
        """
        parametros = []
        
        if self.verificar_tipo(Token.ID):
            parametros.append(self.token_atual.valor)
            self.avancar()
            
            while self.verificar_tipo(Token.VIRGULA):
                self.avancar()
                parametros.append(self.consumir(Token.ID, "Esperado identificador após ','").valor)
        
        return parametros
    
    def argumentos(self):
        """
        argumentos -> ( [expr [, expr]*] )
        :return: Uma lista de nós NoExpressao representando os argumentos
        """
        argumentos = []
        
        self.consumir(Token.ABRE_PAREN, "Esperado '('")
        
        if not self.verificar_tipo(Token.FECHA_PAREN):
            argumentos.append(self.expr())
            
            while self.verificar_tipo(Token.VIRGULA):
                self.avancar()
                argumentos.append(self.expr())
        
        self.consumir(Token.FECHA_PAREN, "Esperado ')'")
        
        return argumentos
    
    def retorno(self):
        """
        retorno -> return [expr]
        :return: Um nó NoRetorno representando a instrução de retorno
        """
        self.consumir(Token.RETURN, "Esperado 'return'")
        
        expr = None
        if not self.final_de_bloco() and not self.verificar_tipo(Token.EOF):
            expr = self.expr()
        
        return NoRetorno(expr)
    
    def declaracao_variavel(self):
        """
        declaracao_variavel -> tipo id [= expr]
        :return: Um nó NoDeclaracaoVariavel representando a declaração de variável
        """
        tipo = None
        if self.verificar_tipo(Token.BOOL):
            tipo = "bool"
        elif self.verificar_tipo(Token.INT):
            tipo = "int"
        elif self.verificar_tipo(Token.STRING):
            tipo = "string"
        else:
            self.erro("Esperado tipo de variável (bool, int ou string)")
        
        self.avancar()
        id = self.consumir(Token.ID, "Esperado identificador após o tipo").valor
        
        valor = None
        if self.verificar_tipo(Token.IGUAL):
            self.avancar()
            valor = self.expr()
        
        return NoDeclaracaoVariavel(tipo, id, valor)
    
    def bool_expr(self):
        """
        bool_expr -> expr (relop expr)?
        :return: Um nó NoExpressao representando a expressão booleana
        """
        esquerda = self.expr()
        
        if (self.verificar_tipo(Token.MAIOR) or 
            self.verificar_tipo(Token.MENOR) or 
            self.verificar_tipo(Token.MAIOR_IGUAL) or 
            self.verificar_tipo(Token.MENOR_IGUAL) or 
            self.verificar_tipo(Token.IGUAL_IGUAL) or 
            self.verificar_tipo(Token.DIFERENTE) or 
            self.verificar_tipo(Token.AND) or 
            self.verificar_tipo(Token.OR)):
            
            operador = self.token_atual.valor
            self.avancar()
            direita = self.expr()
            return NoExpressao(esquerda, operador, direita)
        
        return esquerda
    
    def expr(self):
        """
        expr -> termo ((MAIS | MENOS) termo)*
        :return: Um nó NoExpressao representando a expressão
        """
        no = self.termo()
        
        while self.verificar_tipo(Token.MAIS) or self.verificar_tipo(Token.MENOS):
            operador = self.token_atual.valor
            self.avancar()
            direita = self.termo()
            no = NoExpressao(no, operador, direita)
        
        return no
    
    def termo(self):
        """
        termo -> fator ((MULT | DIV) fator)*
        :return: Um nó NoExpressao representando o termo
        """
        no = self.fator()
        
        while self.verificar_tipo(Token.MULT) or self.verificar_tipo(Token.DIV):
            operador = self.token_atual.valor
            self.avancar()
            direita = self.fator()
            no = NoExpressao(no, operador, direita)
        
        return no
    
    def fator(self):
        """
        fator -> INT_CONST | FLOAT_CONST | STRING_CONST | TRUE | FALSE | ID | (expr) | chamada_funcao
        :return: Um nó representando o fator
        """
        token = self.token_atual
        
        if self.verificar_tipo(Token.INT_CONST):
            self.avancar()
            return NoValor("int", token.valor)
        
        elif self.verificar_tipo(Token.FLOAT_CONST):
            self.avancar()
            return NoValor("float", token.valor)
        
        elif self.verificar_tipo(Token.STRING_CONST):
            self.avancar()
            return NoValor("string", token.valor)
        
        elif self.verificar_tipo(Token.TRUE):
            self.avancar()
            return NoValor("bool", True)
        
        elif self.verificar_tipo(Token.FALSE):
            self.avancar()
            return NoValor("bool", False)
        
        elif self.verificar_tipo(Token.ID):
            id = token.valor
            self.avancar()
            
            if self.verificar_tipo(Token.ABRE_PAREN):
                # Chamada de função
                args = self.argumentos()
                return NoChamadaFuncao(id, args)
            
            return NoValor("id", id)
        
        elif self.verificar_tipo(Token.ABRE_PAREN):
            self.avancar()
            expr = self.expr()
            self.consumir(Token.FECHA_PAREN, "Esperado ')'")
            return expr
        
        elif self.verificar_tipo(Token.NOT):
            self.avancar()
            expr = self.fator()
            return NoExpressao(expr, "not", None)
        
        else:
            self.erro("Expressão inválida")


# Função para testar o analisador sintático com um exemplo simples
def testar_parser(codigo_fonte):
    """
    Testa o analisador sintático com um código fonte
    :param codigo_fonte: O código fonte a ser analisado
    """
    lexer = MiniParLexer(codigo_fonte)
    parser = MiniParParser(lexer)
    try:
        ast = parser.parsear()
        print("Análise sintática bem-sucedida!")
        print("AST:", ast)
    except Exception as e:
        print("Erro durante a análise sintática:", e)


# Exemplo de código para teste (um trecho do Programa de Teste 1)
if __name__ == "__main__":
    codigo_teste = """
    programa-minipar
    # Programa cliente servidor de uma calculadora aritmética simples
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
    
    print("Testando o analisador sintático:")
    testar_parser(codigo_teste)
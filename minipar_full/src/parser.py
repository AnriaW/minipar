import ply.yacc as yacc
from lexer import tokens
from symbol_table import TabelaSimbolos, ErroSemantico

class Parser:
    def __init__(self):
        self.parser = yacc.yacc()  # Cria o parser do PLY

    def parse(self, codigo):
        
        return self.parser.parse(codigo)

# Inicializa a tabela de símbolos global
tabela_simbolos = TabelaSimbolos()

# Precedência de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
)

# Regra inicial
def p_programa_minipar(p):
    'programa_minipar : bloco_stmt'
    p[0] = ('programa', p[1])

# Blocos SEQ e PAR
def p_bloco_stmt(p):
    '''bloco_stmt : bloco_SEQ
                  | bloco_PAR'''
    p[0] = p[1]

def p_bloco_SEQ(p):
    'bloco_SEQ : SEQ LBRACE stmts RBRACE'
    tabela_simbolos.novo_escopo()  # Entra em um novo escopo
    p[0] = ('SEQ', p[3])
    tabela_simbolos.sair_escopo()  # Sai do escopo ao finalizar o bloco

def p_bloco_PAR(p):
    'bloco_PAR : PAR LBRACE stmts RBRACE'
    p[0] = ('PAR', p[3])

# Lista de comandos
def p_stmts(p):
    '''stmts : stmt
             | stmt stmts'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

# Tipos de variáveis
def p_tipo_var(p):
    '''tipo_var : BOOL
                | INT
                | FLOAT_TYPE
                | STRING_TYPE
                | C_CHANNEL
                | LIST LT tipo_var GT'''
    p[0] = p[1] if len(p) == 2 else (p[1], p[3])


# Declaração de variáveis
def p_declaracao(p):
    'declaracao : tipo_var ID ASSIGN expr'
    tipo = p[1]
    nome = p[2]
    try:
        # Declara a variável no escopo atual
        tabela_simbolos.escopo_atual.declarar_variavel(nome, tipo)
    except ErroSemantico as e:
        print(f"Erro Semântico (linha {p.lineno(2)}): {e}")
    p[0] = ('declaracao', tipo, nome, p[4])

    def p_declaracao_String(p):
        'declaracao : STRING_TYPE ID ASSIGN expr'
        tipo = p[1]
        nome = p[2]
        try:
            # Declara a variável no escopo atual
            tabela_simbolos.escopo_atual.declarar_variavel(nome, tipo)
        except ErroSemantico as e:
            print(f"Erro Semântico (linha {p.lineno(2)}): {e}")
        p[0] = ('declaracao', tipo, nome, p[4])

    # Adicione esta regra ao parser.py
def p_declaracao_canal(p):
    '''declaracao : C_CHANNEL ASSIGN ID STRING NUM SEMICOLON'''
    try:
        canal_id = p[3]
        host = p[4].strip('"')  # Remove as aspas da string
        porta = p[5]
        p[0] = ('declaracao_canal', canal_id, host, porta)
    except Exception as e:
        print(f"Erro na declaração do canal: {e}")

        
# Atribuição
def p_atribuicao(p):
    'atribuicao : ID ASSIGN expr'
    p[0] = ('atribuicao', p[1], p[3])

# Comandos
def p_stmt(p):
    '''stmt : declaracao SEMICOLON
            | atribuicao SEMICOLON
            | if_stmt
            | for_stmt
            | while_stmt
            | def_funcao
            | input SEMICOLON
            | output SEMICOLON
            | chamada_funcao SEMICOLON
            | receive_stmt
            | send_stmt
            | RETURN expr SEMICOLON
            | COMMENT'''
    p[0] = p[1]

# Adicionando regra para FOR
def p_for_stmt(p):
    'for_stmt : FOR LPAREN ID IN expr RPAREN LBRACE stmts RBRACE'
    p[0] = ('for', p[3], p[5], p[8])

# Adicionando regra para WHILE
def p_while_stmt(p):
    'while_stmt : WHILE LPAREN expr RPAREN LBRACE stmts RBRACE'
    p[0] = ('while', p[3], p[6])

def p_input(p):
    'input : INPUT LPAREN args RPAREN'
    p[0] = ('input', p[3])

def p_output(p):
    'output : OUTPUT LPAREN args RPAREN'
    p[0] = ('output', p[3])

# Adicionando regra para RECEIVE
def p_receive_stmt(p):
    'receive_stmt : ID DOT RECEIVE COLON expr SEMICOLON'
    p[0] = ('receive', p[2], p[4])

# Adicionando regra para SEND
def p_send_stmt(p):
    'send_stmt : ID DOT SEND COLON expr SEMICOLON'
    p[0] = ('send', p[2], p[4])


# Parâmetros de função
def p_params(p):
    '''params : ID COMMA params
              | ID
              | '''
    if len(p) == 4:
        p[0] = [{'nome': p[1], 'tipo': 'unknown'}] + p[3]  # Tipo temporário
    elif len(p) == 2:
        p[0] = [{'nome': p[1], 'tipo': 'unknown'}]
    else:
        p[0] = []

# Definição de função
def p_def_funcao(p):
    'def_funcao : DEF ID LPAREN params RPAREN LBRACE stmts RBRACE'
    nome_funcao = p[2]
    parametros = p[4]
    # Declara a função na tabela
    try:
        tabela_simbolos.declarar_funcao(
            nome_funcao, 
            tipo_retorno="void",  # Atualize conforme a linguagem
            parametros=parametros
        )
        # Novo escopo para os parâmetros e variáveis locais
        tabela_simbolos.novo_escopo()
        for param in parametros:
            tabela_simbolos.escopo_atual.declarar_variavel(param['nome'], param['tipo'])
        p[0] = ('def_funcao', nome_funcao, parametros, p[7])
    except ErroSemantico as e:
        print(f"Erro em função '{nome_funcao}': {e}")
    finally:
        tabela_simbolos.sair_escopo()  # Sai do escopo da função

def p_expr_input(p):
    'expr : INPUT LPAREN args RPAREN'
    p[0] = ('input', p[3])  # p[3] = lista de argumentos (ex: prompt)

def p_expr_output(p):
    'expr : OUTPUT LPAREN args RPAREN'
    p[0] = ('output', p[3])  # p[3] = valores a serem impressos

# Chamada de função (priorizada antes de expr_simples)
def p_chamada_funcao(p):
    'chamada_funcao : ID LPAREN args RPAREN'
    nome_funcao = p[1]
    args = p[3]
    try:
        # Obtém detalhes da função
        funcao = tabela_simbolos.obter_funcao(nome_funcao)
        # Verifica número de argumentos
        if len(args) != len(funcao['parametros']):
            raise ErroSemantico(f"Função '{nome_funcao}' espera {len(funcao['parametros'])} argumentos, mas {len(args)} foram fornecidos")
        p[0] = ('chamada_funcao', nome_funcao, args)
    except ErroSemantico as e:
        print(f"Erro Semântico (linha {p.lineno(1)}): {e}")
        p[0] = ('erro', nome_funcao)

def p_args(p):
    '''args : expr_list
            | '''
    p[0] = p[1] if len(p) > 1 else []

# Expressões
def p_expr(p):
    '''expr : chamada_funcao
            | expr_binop
            | expr_comparacao
            | expr_lista
            | expr_simples'''
    p[0] = p[1]

def p_expr_binop(p):
    '''expr_binop : expr PLUS expr
                  | expr MINUS expr
                  | expr MULT expr
                  | expr DIV expr'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expr_comparacao(p):
    '''expr_comparacao : expr LT expr
                       | expr LE expr
                       | expr GT expr
                       | expr GE expr
                       | expr EQ expr
                       | expr NE expr'''
    p[0] = ('comparacao', p[2], p[1], p[3])

def p_expr_lista(p):
    'expr_lista : LBRACKET expr_list RBRACKET'
    p[0] = ('lista', p[2])

def p_expr_list(p):
    '''expr_list : expr
                 | expr COMMA expr_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_expr_simples(p):
    '''expr_simples : ID
                    | NUM
                    | FLOAT
                    | STRING
                    | TRUE
                    | FALSE
                    | ID DOT ID'''
    if len(p) == 4:  # Caso do ID DOT ID
        p[0] = ('acesso_atributo', p[1], p[3])
    elif isinstance(p[1], str) and p[1].lower() in ('true', 'false'):
        p[0] = ('bool', p[1].lower() == 'true')
    elif isinstance(p[1], str):
        # Verifica se é uma string
        if p.slice[1].type == 'STRING':
            p[0] = ('string', p[1])  # Literal string
        # Verifica se é um booleano
        elif p[1].lower() in ('true', 'false'):
            p[0] = ('bool', p[1].lower() == 'true')
        # Caso contrário, é um ID (variável)
        else:
            try:
                simbolo = tabela_simbolos.escopo_atual.obter_variavel(p[1])
                p[0] = ('id', p[1], simbolo['tipo'])
            except ErroSemantico as e:
                print(f"Erro Semântico (linha {p.lineno(1)}): {e}")
                p[0] = ('erro', p[1])
    else:
        p[0] = p[1]

# Estrutura condicional
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN LBRACE stmts RBRACE
               | IF LPAREN expr RPAREN LBRACE stmts RBRACE ELSE LBRACE stmts RBRACE'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6], None)
    else:
        p[0] = ('if', p[3], p[6], p[10])

# Tratamento de erros
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do código")


# Cria o parser
parser = yacc.yacc()
# lexer.py
import ply.lex as lex

# Lista de tokens atualizada
tokens = (
    # Palavras-chave
    'SEQ', 'PAR', 'IF', 'ELSE', 'WHILE', 'DEF', 'RETURN', 'INPUT', 'OUTPUT',
    'SEND', 'RECEIVE', 'BOOL', 'INT', 'FLOAT_TYPE', 'STRING_TYPE',
    'C_CHANNEL', 'LIST', 'FOR', 'IN', 'TRUE', 'FALSE',
    
    # Identificadores e literais
    'ID', 'NUM', 'FLOAT', 'STRING',
    
    # Operadores e símbolos
    'PLUS', 'MINUS', 'MULT', 'DIV', 'ASSIGN', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'COLON', 'DOT',
    'SEMICOLON',  # Adicionado
    
    # Comentários
    'COMMENT'
)


# Palavras-chave (mapeamento de palavras para tokens)
keywords = {
    'SEQ': 'SEQ',
    'PAR': 'PAR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'input': 'INPUT',
    'output': 'OUTPUT',
    'def': 'DEF',
    'return': 'RETURN',
    'send': 'SEND',
    'receive': 'RECEIVE',
    'Bool': 'BOOL',
    'Int': 'INT',
    'Float': 'FLOAT_TYPE',
    'String': 'STRING_TYPE',
    'c_channel': 'C_CHANNEL',
    'List': 'LIST',
    'for': 'FOR',
    'in': 'IN',
    'true': 'TRUE',
    'false': 'FALSE'
}

# Operadores simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_ASSIGN = r'='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'
t_SEMICOLON = r';' 

# Identificadores e palavras-chave
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')  # Verifica se é palavra-chave
    return t


# Números de ponto flutuante (suporta notação científica)
def t_FLOAT(t):
    r'-?\d+\.\d+|\.\d+|-?\d+\.'
    t.value = float(t.value)
    return t

# Números inteiros
def t_NUM(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


# Strings (suporta escape com \")
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Comentários (ignorados)
def t_COMMENT(t):
    r'\#.*'
    pass  # Ignora comentários

# Ignora espaços e tabs
t_ignore = ' \t'

# Controle de linhas (para mensagens de erro)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Cria o lexer
lexer = lex.lex()
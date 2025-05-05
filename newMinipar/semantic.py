"""
semantic.py - Analisador Semântico para a linguagem MiniPar
Responsável pela análise semântica do código fonte escrito na linguagem MiniPar,
verificando tipos, escopo de variáveis e validade das operações.
"""

from parser import (
    NoPrograma, NoBlocoSEQ, NoBlocoPAR, NoDeclaracaoCanal, NoEnvio, NoRecepcao,
    NoAtribuicao, NoExpressao, NoValor, NoCondicional, NoEnquanto, NoSaida, NoEntrada,
    NoFuncao, NoChamadaFuncao, NoRetorno, NoDeclaracaoVariavel
)

class Simbolo:
    """Representa um símbolo na tabela de símbolos"""
    def __init__(self, nome, tipo, valor=None, escopo=None, parametros=None):
        self.nome = nome
        self.tipo = tipo  # 'int', 'bool', 'string', 'func', 'c_channel'
        self.valor = valor
        self.escopo = escopo
        self.parametros = parametros or []  # Lista de parâmetros para funções
    
    def __str__(self):
        if self.tipo == 'func':
            return f"Simbolo(nome={self.nome}, tipo={self.tipo}, parametros={self.parametros}, escopo={self.escopo})"
        else:
            return f"Simbolo(nome={self.nome}, tipo={self.tipo}, valor={self.valor}, escopo={self.escopo})"


class TabelaSimbolos:
    """Gerencia os símbolos do programa, organizados por escopo"""
    def __init__(self):
        self.tabela = {}  # Dicionário de símbolos: {escopo: {nome: simbolo}}
        self.escopo_atual = "global"
        
        # Inicializa o escopo global
        self.tabela[self.escopo_atual] = {}
        
        # Adiciona funções internas da linguagem
        self._adicionar_funcoes_internas()
    
    def _adicionar_funcoes_internas(self):
        """Adiciona funções internas da linguagem à tabela de símbolos"""
        # Função de ativação (sigmoid, relu, etc.)
        self.inserir("activation", "func", parametros=["sum"])
        self.inserir("sigmoid", "func", parametros=["x"])
        self.inserir("sigmoid_derivative", "func", parametros=["x"])
        self.inserir("relu", "func", parametros=["x"])
        self.inserir("quicksort", "func", parametros=["array"])
        self.inserir("print", "func", parametros=["*args"])
        self.inserir("input", "func", parametros=[])
    
    def entrar_escopo(self, escopo):
        """Entra em um novo escopo"""
        self.escopo_atual = escopo
        if escopo not in self.tabela:
            self.tabela[escopo] = {}
    
    def sair_escopo(self):
        """Sai do escopo atual e retorna ao escopo global"""
        self.escopo_atual = "global"
    
    def inserir(self, nome, tipo, valor=None, parametros=None):
        """Insere um símbolo no escopo atual"""
        simbolo = Simbolo(nome, tipo, valor, self.escopo_atual, parametros)
        self.tabela[self.escopo_atual][nome] = simbolo
        return simbolo
    
    def buscar(self, nome):
        """Busca um símbolo pelo nome, procurando no escopo atual e depois no global"""
        # Primeiro procura no escopo atual
        if nome in self.tabela.get(self.escopo_atual, {}):
            return self.tabela[self.escopo_atual][nome]
        
        # Se não encontrar, procura no escopo global
        if nome in self.tabela["global"]:
            return self.tabela["global"][nome]
        
        return None
    
    def atualizar(self, nome, valor):
        """Atualiza o valor de um símbolo existente"""
        simbolo = self.buscar(nome)
        if simbolo:
            simbolo.valor = valor
            return True
        return False
    
    def simbolo_ja_existe_no_escopo_atual(self, nome):
        """Verifica se um símbolo já existe no escopo atual"""
        return nome in self.tabela.get(self.escopo_atual, {})


class AnalisadorSemantico:
    """
    Analisador semântico para a linguagem MiniPar
    Verifica a semântica do programa, como tipos, escopo de variáveis e validade das operações
    """
    
    def __init__(self):
        """Inicializa o analisador semântico"""
        self.tabela_simbolos = TabelaSimbolos()
        self.erros = []
        self.canais = {}  # Dicionário para armazenar informações sobre canais: {nome: (comp1, comp2)}
        self.funcoes = {}  # Dicionário para armazenar informações sobre funções: {nome: (parametros, corpo)}
    
    def erro(self, mensagem):
        """
        Registra um erro semântico
        :param mensagem: A mensagem de erro
        """
        self.erros.append(f"Erro semântico: {mensagem}")
    
    def analisar(self, ast):
        """
        Inicia o processo de análise semântica do programa
        :param ast: A árvore sintática abstrata (AST) do programa
        :return: True se não houver erros semânticos, False caso contrário
        """
        if isinstance(ast, NoPrograma):
            self.visitar_programa(ast)
        else:
            self.erro("AST inválida: esperado um nó de programa")
        
        if self.erros:
            for erro in self.erros:
                print(erro)
            return False
        
        return True
    
    def visitar_programa(self, no):
        """
        Analisa semanticamente um nó de programa
        :param no: O nó de programa a ser analisado
        """
        self.visitar(no.bloco)
    
    def visitar(self, no):
        """
        Visita um nó da AST e executa a análise semântica apropriada
        :param no: O nó a ser visitado
        :return: O tipo resultante da expressão, se aplicável
        """
        if isinstance(no, NoBlocoSEQ):
            return self.visitar_bloco_seq(no)
        elif isinstance(no, NoBlocoPAR):
            return self.visitar_bloco_par(no)
        elif isinstance(no, NoDeclaracaoCanal):
            return self.visitar_declaracao_canal(no)
        elif isinstance(no, NoEnvio):
            return self.visitar_envio(no)
        elif isinstance(no, NoRecepcao):
            return self.visitar_recepcao(no)
        elif isinstance(no, NoAtribuicao):
            return self.visitar_atribuicao(no)
        elif isinstance(no, NoExpressao):
            return self.visitar_expressao(no)
        elif isinstance(no, NoValor):
            return self.visitar_valor(no)
        elif isinstance(no, NoCondicional):
            return self.visitar_condicional(no)
        elif isinstance(no, NoEnquanto):
            return self.visitar_enquanto(no)
        elif isinstance(no, NoSaida):
            return self.visitar_saida(no)
        elif isinstance(no, NoEntrada):
            return self.visitar_entrada(no)
        elif isinstance(no, NoFuncao):
            return self.visitar_funcao(no)
        elif isinstance(no, NoChamadaFuncao):
            return self.visitar_chamada_funcao(no)
        elif isinstance(no, NoRetorno):
            return self.visitar_retorno(no)
        elif isinstance(no, NoDeclaracaoVariavel):
            return self.visitar_declaracao_variavel(no)
        elif isinstance(no, list):
            # Para listas de nós (como em blocos)
            for item in no:
                self.visitar(item)
            return None
        else:
            self.erro(f"Tipo de nó desconhecido: {type(no)}")
            return None
    
    def visitar_bloco_seq(self, no):
        """
        Analisa semanticamente um nó de bloco sequencial
        :param no: O nó de bloco sequencial a ser analisado
        """
        for stmt in no.stmts:
            self.visitar(stmt)
    
    def visitar_bloco_par(self, no):
        """
        Analisa semanticamente um nó de bloco paralelo
        :param no: O nó de bloco paralelo a ser analisado
        """
        for stmt in no.stmts:
            self.visitar(stmt)
    
    def visitar_declaracao_canal(self, no):
        """
        Analisa semanticamente um nó de declaração de canal
        :param no: O nó de declaração de canal a ser analisado
        """
        # Verifica se o canal já foi declarado
        if no.nome in self.canais:
            self.erro(f"Canal '{no.nome}' já foi declarado")
        else:
            # Registra o canal na tabela de símbolos
            self.tabela_simbolos.inserir(no.nome, "c_channel")
            self.canais[no.nome] = (no.comp1, no.comp2)
    
    def visitar_envio(self, no):
        """
        Analisa semanticamente um nó de envio de mensagem
        :param no: O nó de envio a ser analisado
        """
        # Verifica se o canal existe
        if no.canal not in self.canais:
            self.erro(f"Canal '{no.canal}' não foi declarado")
        else:
            # Verifica os argumentos do envio
            for arg in no.args:
                self.visitar(arg)
    
    def visitar_recepcao(self, no):
        """
        Analisa semanticamente um nó de recepção de mensagem
        :param no: O nó de recepção a ser analisado
        """
        # Verifica se o canal existe
        if no.canal not in self.canais:
            self.erro(f"Canal '{no.canal}' não foi declarado")
        else:
            # Verifica os argumentos da recepção
            for arg in no.args:
                # Para recepção, os argumentos devem ser identificadores
                if isinstance(arg, NoValor) and arg.tipo == "id":
                    # Verifica se a variável existe ou cria uma nova
                    simbolo = self.tabela_simbolos.buscar(arg.valor)
                    if not simbolo:
                        # Assumimos que a variável será do tipo 'var' (genérico)
                        self.tabela_simbolos.inserir(arg.valor, "var")
                else:
                    self.erro(f"Argumento inválido na recepção: esperado um identificador")
    
    def visitar_atribuicao(self, no):
        """
        Analisa semanticamente um nó de atribuição
        :param no: O nó de atribuição a ser analisado
        """
        # Avalia o tipo da expressão
        tipo_expr = self.visitar(no.expr)
        
        # Verifica se a variável já foi declarada
        simbolo = self.tabela_simbolos.buscar(no.id)
        if simbolo:
            # Verifica compatibilidade de tipos
            if simbolo.tipo not in ["var", tipo_expr] and simbolo.tipo != "any":
                self.erro(f"Incompatibilidade de tipos: tentativa de atribuir '{tipo_expr}' a variável '{no.id}' do tipo '{simbolo.tipo}'")
            else:
                # Atualiza o valor da variável
                self.tabela_simbolos.atualizar(no.id, None)  # Valor será atualizado em tempo de execução
        else:
            # Cria uma nova variável com o tipo inferido
            self.tabela_simbolos.inserir(no.id, tipo_expr)
    
    def visitar_expressao(self, no):
        """
        Analisa semanticamente um nó de expressão
        :param no: O nó de expressão a ser analisado
        :return: O tipo resultante da expressão
        """
        if no.operador is None:
            # Expressão simples (apenas um termo)
            return self.visitar(no.esquerda)
        
        # Avalia os tipos dos operandos
        tipo_esq = self.visitar(no.esquerda)
        
        if no.operador == "not":
            # Operador unário 'not'
            if tipo_esq != "bool":
                self.erro(f"Operador 'not' só pode ser aplicado a expressões booleanas, não a '{tipo_esq}'")
            return "bool"
        
        # Operadores binários
        tipo_dir = self.visitar(no.direita)
        
        # Operadores aritméticos
        if no.operador in ["+", "-", "*", "/"]:
            if tipo_esq not in ["int", "float"] or tipo_dir not in ["int", "float"]:
                self.erro(f"Operador '{no.operador}' só pode ser aplicado a números, não a '{tipo_esq}' e '{tipo_dir}'")
            
            # Se um dos operandos for float, o resultado é float
            if tipo_esq == "float" or tipo_dir == "float":
                return "float"
            return "int"
        
        # Operadores relacionais
        elif no.operador in [">", "<", ">=", "<=", "==", "!="]:
            # Verificações específicas para diferentes tipos
            if tipo_esq != tipo_dir and not (tipo_esq in ["int", "float"] and tipo_dir in ["int", "float"]):
                self.erro(f"Incompatibilidade de tipos para o operador '{no.operador}': '{tipo_esq}' e '{tipo_dir}'")
            
            return "bool"
        
        # Operadores lógicos
        elif no.operador in ["and", "or"]:
            if tipo_esq != "bool" or tipo_dir != "bool":
                self.erro(f"Operador '{no.operador}' só pode ser aplicado a expressões booleanas, não a '{tipo_esq}' e '{tipo_dir}'")
            
            return "bool"
        
        # Operador de concatenação para strings
        elif no.operador == "+" and (tipo_esq == "string" or tipo_dir == "string"):
            if tipo_esq != "string" or tipo_dir != "string":
                self.erro(f"Incompatibilidade de tipos para concatenação: '{tipo_esq}' e '{tipo_dir}'")
            
            return "string"
        
        self.erro(f"Operador desconhecido: '{no.operador}'")
        return None
    
    def visitar_valor(self, no):
        """
        Analisa semanticamente um nó de valor
        :param no: O nó de valor a ser analisado
        :return: O tipo do valor
        """
        if no.tipo == "id":
            # Verifica se a variável existe
            simbolo = self.tabela_simbolos.buscar(no.valor)
            if not simbolo:
                self.erro(f"Variável '{no.valor}' não foi declarada")
                return "unknown"
            return simbolo.tipo
        
        return no.tipo
    
    def visitar_condicional(self, no):
        """
        Analisa semanticamente um nó condicional
        :param no: O nó condicional a ser analisado
        """
        # Avalia o tipo da condição
        tipo_condicao = self.visitar(no.condicao)
        if tipo_condicao != "bool":
            self.erro(f"Condição do if deve ser booleana, não '{tipo_condicao}'")
        
        # Analisa o bloco verdadeiro
        self.visitar(no.bloco_verdadeiro)
        
        # Analisa o bloco falso, se existir
        if no.bloco_falso:
            self.visitar(no.bloco_falso)
    
    def visitar_enquanto(self, no):
        """
        Analisa semanticamente um nó de repetição (while)
        :param no: O nó de repetição a ser analisado
        """
        # Avalia o tipo da condição
        tipo_condicao = self.visitar(no.condicao)
        if tipo_condicao != "bool":
            self.erro(f"Condição do while deve ser booleana, não '{tipo_condicao}'")
        
        # Analisa o bloco do while
        self.visitar(no.bloco)
    
    def visitar_saida(self, no):
        """
        Analisa semanticamente um nó de saída (output)
        :param no: O nó de saída a ser analisado
        """
        # Qualquer tipo pode ser impresso
        self.visitar(no.expr)
    
    def visitar_entrada(self, no):
        """
        Analisa semanticamente um nó de entrada (input)
        :param no: O nó de entrada a ser analisado
        """
        # Verifica se a variável existe, senão cria
        simbolo = self.tabela_simbolos.buscar(no.id)
        if not simbolo:
            # Assume o tipo string para entrada (pode ser convertido depois)
            self.tabela_simbolos.inserir(no.id, "string")
    
    def visitar_funcao(self, no):
        """
        Analisa semanticamente um nó de definição de função
        :param no: O nó de função a ser analisado
        """
        # Verifica se a função já foi declarada
        if no.nome in self.funcoes:
            self.erro(f"Função '{no.nome}' já foi declarada")
        else:
            # Registra a função na tabela de símbolos
            self.tabela_simbolos.inserir(no.nome, "func", parametros=no.parametros)
            self.funcoes[no.nome] = (no.parametros, no.corpo)
            
            # Cria um novo escopo para a função
            escopo_func = f"func_{no.nome}"
            self.tabela_simbolos.entrar_escopo(escopo_func)
            
            # Registra os parâmetros no escopo da função
            for param in no.parametros:
                self.tabela_simbolos.inserir(param, "var")
            
            # Analisa o corpo da função
            self.visitar(no.corpo)
            
            # Volta ao escopo anterior
            self.tabela_simbolos.sair_escopo()
    
    def visitar_chamada_funcao(self, no):
        """
        Analisa semanticamente um nó de chamada de função
        :param no: O nó de chamada de função a ser analisado
        :return: O tipo de retorno da função (assumido como "any" por enquanto)
        """
        # Verifica se a função existe
        simbolo = self.tabela_simbolos.buscar(no.nome)
        if not simbolo or simbolo.tipo != "func":
            self.erro(f"Função '{no.nome}' não foi declarada")
            return "unknown"
        
        # Verifica o número de argumentos
        if len(no.argumentos) != len(simbolo.parametros) and "*args" not in simbolo.parametros:
            self.erro(f"Número incorreto de argumentos para função '{no.nome}': esperado {len(simbolo.parametros)}, recebido {len(no.argumentos)}")
        
        # Analisa os argumentos
        for arg in no.argumentos:
            self.visitar(arg)
        
        # Por simplicidade, assumimos que todas as funções retornam "any"
        return "any"
    
    def visitar_retorno(self, no):
        """
        Analisa semanticamente um nó de retorno
        :param no: O nó de retorno a ser analisado
        """
        # Verifica se estamos dentro de uma função
        if not self.tabela_simbolos.escopo_atual.startswith("func_"):
            self.erro("Instrução 'return' fora de uma função")
        
        # Analisa a expressão de retorno, se existir
        if no.expr:
            self.visitar(no.expr)
    
    def visitar_declaracao_variavel(self, no):
        """
        Analisa semanticamente um nó de declaração de variável
        :param no: O nó de declaração de variável a ser analisado
        """
        # Verifica se a variável já foi declarada no escopo atual
        if self.tabela_simbolos.simbolo_ja_existe_no_escopo_atual(no.id):
            self.erro(f"Variável '{no.id}' já foi declarada neste escopo")
        else:
            # Registra a variável na tabela de símbolos
            if no.valor:
                # Analisa o valor inicial
                tipo_valor = self.visitar(no.valor)
                
                # Verifica compatibilidade de tipos
                if no.tipo != tipo_valor and tipo_valor != "any":
                    self.erro(f"Incompatibilidade de tipos: tentativa de atribuir '{tipo_valor}' a variável '{no.id}' do tipo '{no.tipo}'")
            
            self.tabela_simbolos.inserir(no.id, no.tipo)


# Função para testar o analisador semântico com um exemplo simples
def testar_semantic(ast):
    """
    Testa o analisador semântico com uma AST
    :param ast: A árvore sintática abstrata a ser analisada
    """
    analisador = AnalisadorSemantico()
    resultado = analisador.analisar(ast)
    
    if resultado:
        print("Análise semântica bem-sucedida!")
        print("Tabela de símbolos:", analisador.tabela_simbolos.tabela)
    else:
        print("Erros semânticos encontrados.")


# Esta parte será executada somente se o arquivo for executado diretamente
if __name__ == "__main__":
    from lexer import MiniParLexer
    from parser import MiniParParser
    
    # Exemplo de código para teste (um trecho do Programa de Teste 1)
    codigo_teste = """
    programa-minipar
    # Programa cliente servidor de uma calculadora aritmética simples
    c_channel calculadora computador_1 computador_2
    SEQ{
        operacao = "+"
        valor1 = 10
        valor2 = 20
        resultado = valor1 + valor2
        calculadora.send(operacao, valor1, valor2, resultado)
        output resultado
    }
    """
    
    print("Testando o analisador semântico:")
    lexer = MiniParLexer(codigo_teste)
    parser = MiniParParser(lexer)
    
    try:
        ast = parser.parsear()
        testar_semantic(ast)
    except Exception as e:
        print("Erro durante a análise:", e)
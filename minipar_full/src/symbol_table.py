class Escopo:
    """
    Representa um escopo (global, função, bloco) e armazena símbolos (variáveis, parâmetros).
    """
    def __init__(self, pai=None):
        self.simbolos = {}  # Dicionário: {nome: {'tipo': tipo, 'valor': valor}}
        self.pai = pai      # Escopo pai para hierarquia (encadeamento de escopos)

    def declarar_variavel(self, nome, tipo, valor=None):
        """
        Declara uma variável no escopo atual.
        Levanta ErroSemantico se a variável já existir.
        """
        if nome in self.simbolos:
            raise ErroSemantico(f"Variável '{nome}' já declarada neste escopo")
        self.simbolos[nome] = {'tipo': tipo, 'valor': valor}

    def obter_variavel(self, nome):
        """
        Busca uma variável no escopo atual ou em escopos pais.
        Levanta ErroSemantico se não encontrada.
        """
        escopo = self
        while escopo:
            if nome in escopo.simbolos:
                return escopo.simbolos[nome]
            escopo = escopo.pai
        raise ErroSemantico(f"Variável '{nome}' não declarada")

class TabelaSimbolos:
    """
    Gerencia todos os escopos e funções do programa.
    """
    def __init__(self):
        self.escopo_global = Escopo()   # Escopo global padrão
        self.escopo_atual = self.escopo_global
        self.funcoes = {}               # Dicionário: {nome: {'tipo_retorno': tipo, 'parametros': [tipos]}}

    def novo_escopo(self):
        """Cria um novo escopo filho (ex: ao entrar em um bloco ou função)."""
        self.escopo_atual = Escopo(self.escopo_atual)

    def sair_escopo(self):
        """Retorna ao escopo pai (ex: ao sair de um bloco ou função)."""
        if self.escopo_atual.pai:
            self.escopo_atual = self.escopo_atual.pai
        else:
            raise ErroSemantico("Não é possível sair do escopo global")

    def declarar_funcao(self, nome, tipo_retorno, parametros):
        """
        Declara uma função no escopo global.
        parametros: Lista de dicionários [{'nome': str, 'tipo': str}]
        """
        if nome in self.funcoes:
            raise ErroSemantico(f"Função '{nome}' já declarada")
        self.funcoes[nome] = {
            'tipo_retorno': tipo_retorno,
            'parametros': parametros
        }

    def obter_funcao(self, nome):
        """Retorna os detalhes de uma função ou levanta erro se não existir."""
        if nome not in self.funcoes:
            raise ErroSemantico(f"Função '{nome}' não declarada")
        return self.funcoes[nome]

class ErroSemantico(Exception):
    """Exceção para erros semânticos (variáveis não declaradas, tipos incompatíveis, etc.)."""
    pass
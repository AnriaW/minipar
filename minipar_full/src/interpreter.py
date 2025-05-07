# src/interpreter.py
import threading
from channels import Canal
from symbol_table import TabelaSimbolos, ErroSemantico

class Executor:
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.canais = {}  # Dicionário de canais: {id: Canal}
        self.contexto = {}  # Contexto de execução (variáveis temporárias)

    def executar(self, arvore):
        """Executa a árvore sintática gerada pelo parser."""
        try:
            self.visitar(arvore)
        except ErroExecucao as e:
            print(f"Erro durante a execução: {e}")

    def visitar(self, no):
        """Despacha a execução com base no tipo do nó."""
        metodo = f'visitar_{type(no).__name__}'
        return getattr(self, metodo, self.visitar_generico)(no)

    def visitar_generico(self, no):
        """Visita nós genéricos (para estruturas não implementadas)."""
        pass

    # --------------------------------------
    # Blocos Fundamentais
    # --------------------------------------
    def visitar_BlocoSEQ(self, no):
        """Executa instruções sequencialmente."""
        for stmt in no.stmts:
            self.visitar(stmt)

    def visitar_BlocoPAR(self, no):
        """Executa instruções em paralelo usando threads."""
        threads = []
        for stmt in no.stmts:
            thread = threading.Thread(target=self.visitar, args=(stmt,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()  # Aguarda todas finalizarem

    # --------------------------------------
    # Declarações e Atribuições
    # --------------------------------------
    def visitar_DeclaracaoVariavel(self, no):
        """Declara uma variável na tabela de símbolos."""
        tipo = no.tipo
        nome = no.id
        valor = self.visitar(no.expr) if no.expr else None
        self.tabela.escopo_atual.declarar_variavel(nome, tipo, valor)

    def visitar_Atribuicao(self, no):
        """Atribui valor a uma variável."""
        nome = no.id
        valor = self.visitar(no.expr)
        self.tabela.escopo_atual.simbolos[nome]['valor'] = valor

    # --------------------------------------
    # Comunicação via Canais
    # --------------------------------------
    def visitar_DeclaracaoCanal(self, no):
        """Cria um canal de comunicação (servidor ou cliente)."""
        canal_id = no.id
        host = no.host
        port = no.port
        self.canais[canal_id] = Canal(canal_id, host, port)
        print(f"[Canal {canal_id}] Configurado em {host}:{port}")

# interpreter.py

def visitar_Send(self, no):
    canal_id = no.canal  # p[1] (ex: "teste" em teste.SEND: ...)
    dados = self.visitar(no.dados)  # p[4] (ex: "Olá do cliente!")
    
    if canal_id not in self.canais:
        raise ErroExecucao(f"Canal '{canal_id}' não declarado!")
    
    self.canais[canal_id].enviar(str(dados))

def visitar_Receive(self, no):
    canal_id = no.canal  # p[1] (ex: "teste" em teste.RECEIVE: ...)
    variavel_destino = no.variavel  # p[4] (ex: "resultado" para armazenar dados)
    
    if canal_id not in self.canais:
        raise ErroExecucao(f"Canal '{canal_id}' não declarado!")
    
    dados = self.canais[canal_id].receber()
    self.tabela.escopo_atual.simbolos[variavel_destino]['valor'] = dados  # Atribui à variável

    # --------------------------------------
    # E/S e Funções
    # --------------------------------------
    def visitar_Input(self, no):
        """Lê entrada do usuário."""
        prompt = ' '.join([self.visitar(arg) for arg in no.args])
        return input(prompt)

    def visitar_Output(self, no):
        """Exibe saída na tela."""
        mensagem = ' '.join([str(self.visitar(arg)) for arg in no.args])
        print(mensagem)

    def visitar_ChamadaFuncao(self, no):
        """Executa uma função declarada."""
        nome = no.nome
        args = [self.visitar(arg) for arg in no.args]
        
        if nome not in self.tabela.funcoes:
            raise ErroExecucao(f"Função '{nome}' não declarada!")
        
        # Implemente a lógica de chamada de função aqui
        return 0  # Placeholder

    # --------------------------------------
    # Utilitários
    # --------------------------------------
    def visitar_Numero(self, no):
        return no.valor

    def visitar_String(self, no):
        return no.valor

    def visitar_ID(self, no):
        """Obtém valor de uma variável."""
        return self.tabela.escopo_atual.obter_variavel(no.nome)['valor']

class ErroExecucao(Exception):
    pass

# Ponto de entrada do interpretador
if __name__ == "__main__":
    from parser import Parser
    # Exemplo de uso
    codigo = """
    SEQ {
        c_channel = cliente "localhost" 12345;
        string resposta = ""  # Variável para armazenar resposta
        cliente.send: "Olá servidor!";  # Envia mensagem
        cliente.receive: resposta;      # Recebe resposta
        output("Resposta:", resposta);
        }
    """
    
    parser = Parser()
    arvore = parser.parse(codigo)
    
    executor = Executor()
    executor.executar(arvore)
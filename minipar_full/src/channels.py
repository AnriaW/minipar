import socket

class Canal:
    def __init__(self, id, host, port):
        self.id = id
        self.host = host
        self.port = port
        self.socket = None
        self.connection = None  # Usado no modo servidor

    def iniciar_servidor(self):
        """Configura o servidor para receber conexões."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"[{self.id}] Servidor aguardando conexões em {self.host}:{self.port}...")
        self.connection, addr = self.socket.accept()
        print(f"[{self.id}] Conexão estabelecida com {addr}")

    def conectar(self):
        """Conecta ao servidor como cliente."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"[{self.id}] Conectado a {self.host}:{self.port}")

    def enviar(self, dados):
        """Envia dados pelo socket."""
        if isinstance(dados, (list, dict)):
            dados = str(dados)  # Serialização simplificada (pode usar JSON)
        if self.connection:  # Modo servidor
            self.connection.sendall(dados.encode())
        elif self.socket:    # Modo cliente
            self.socket.sendall(dados.encode())
        print(f"[{self.id}] Dados enviados: {dados}")

    def receber(self):
        """Recebe dados do socket."""
        origem = self.connection if self.connection else self.socket
        dados = origem.recv(1024).decode()
        print(f"[{self.id}] Dados recebidos: {dados}")
        return dados

    def fechar(self):
        """Fecha os sockets."""
        if self.connection:
            self.connection.close()
        if self.socket:
            self.socket.close()
        print(f"[{self.id}] Conexão fechada.")
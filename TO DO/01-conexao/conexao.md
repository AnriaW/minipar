# Programa de Teste 1.
programa-miniPar
Programa cliente servidor de uma calculadora aritmética simples
O cliente (computador_1) solicita a execução de uma operação aritmética e
o servidor (computador_2) realiza o
calculo retornando o resultado para o cliente
c_channel calculadora computador_1 computador_2
declaração do canal de comunicação calculadora associada a dos computadores
(computador_1 e computador_2).

SEQ
depois do SEQ todas as seguintes instruções indentadas serão executadas de
forma seqüencial
Apresentar na tela via print as opções da calculadora +, -, *, /
Ler a operação aritmética desejada via sys.stdin.readline()
Ler o operando 1 (valor) e operando 2 (valor) via sys.stdin.readline()

calculadora.send (operação, valor1, valor2, resultado)
computador cliente (computador_1)
Imprime o resultado via print

---- Execução: Servidor (computador 2)
computador servidor
calculadora.receive (operação, valor1, valor2, resultado)
computador 2 recebe a solicitação do cliente (computador 1) e executa o cálculo e
retorna o resultado ao cliente (computador 1)

Execução: Testar com localhost para o computador 2 (Servidor)
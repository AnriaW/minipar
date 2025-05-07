c_channel calculadora localhost 9999

SEQ {
    output("Servidor pronto. Aguardando operação...");
    operacao, val1, val2 = calculadora.receive();
    resultado = calcular(operacao, val1, val2);
    calculadora.send(resultado);
}
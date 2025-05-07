c_channel calculadora localhost 9999

SEQ {
    operacao = input("Operação (+, -, *, /): ");
    val1 = float(input("Valor 1: "));
    val2 = float(input("Valor 2: "));
    calculadora.send([operacao, val1, val2]);
    resultado = calculadora.receive();
    output("Resultado: ", resultado);
}
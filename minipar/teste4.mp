PAR {
    input_val = 1
    output_desire = 0
    input_weight = 0.5
    learning_rate = 0.01
    error = 1000
    iteration = 0
    bias = 1
    bias_weight = 0.5

    WHILE (error != 0) {
        iteration = iteration + 1
        Output "#### Iteração: "
        Output iteration

        Output "Peso: "
        Output input_weight

        sum_val = (input_val * input_weight) + (bias * bias_weight)

        IF (sum_val >= 0) {
            output = 1
        } ELSE {
            output = 0
        }

        Output "Saída: "
        Output output

        error = output_desire - output

        Output "Erro: "
        Output error

        IF (error != 0) {
            input_weight = input_weight + (learning_rate * input_val * error)

            Output "Peso do bias: "
            Output bias_weight

            bias_weight = bias_weight + (learning_rate * bias * error)
        }
    }

    Output "Parabéns!!! A Rede de um Neurônio Aprendeu"
    Output "Valor desejado: "
    Output output_desire
}

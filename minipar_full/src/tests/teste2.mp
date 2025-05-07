PAR {
    # Thread 1: Cálculo do Fatorial de um número
    SEQ {
        # Declaração das variáveis
        int numero = 5;
        int fatorial = 1;
        int i = 1;
        
        # Entrada do número para calcular o fatorial
        output("Thread 1 - Cálculo do Fatorial");
        output("Digite um número para calcular seu fatorial: ");
        numero = input();
        
        # Cálculo do fatorial usando um loop while
        while (i <= numero) {
            fatorial = fatorial * i;
            i = i + 1;
        }
        
        # Saída do resultado
        output("O fatorial de ");
        output(numero);
        output(" é: ");
        output(fatorial);
    }
    
    # Thread 2: Cálculo da Série de Fibonacci
    SEQ {
        # Declaração das variáveis
        int limite = 10;
        int a = 0;
        int b = 1;
        int temp = 0;
        int contador = 0;
        
        # Entrada do número de termos da série
        output("Thread 2 - Cálculo da Série de Fibonacci");
        output("Digite quantos termos da série de Fibonacci deseja calcular: ");
        limite = input();
        
        output("Série de Fibonacci com ");
        output(limite);
        output(" termos: ");
        
        # Cálculo e exibição da série
        while (contador < limite) {
            output(a);
            output(" ");
            
            temp = a + b;
            a = b;
            b = temp;
            
            contador = contador + 1;
        }
    }
}
int rxPin = 4;  // Pino digital para recepção
int baudRate = 9600;  // Define o baud rate

void setup() {
    pinMode(rxPin, INPUT); // Configura o pino como entrada
    Serial.begin(9600); // Para monitoramento pelo monitor serial do Arduino
}

// Função para substituir o uso delay()
void _sw_uart_wait_half_T() {
    for (int i = 0; i < 1093; i++) {
        asm("NOP");
    }
}

// Função para calcular a paridade par (even parity) usando o método do professor
int calc_even_parity(char data) {
    int ones = 0;
    for (int i = 0; i < 8; i++) {
        ones += (data >> i) & 0x01;
    }
    return ones % 2;
}

// Função para ler um caractere completo e verificar paridade
char readChar() {
    // Espera pelo bit de start (LOW)
    while (digitalRead(rxPin) == HIGH) {
        // Fica aqui até detectar um LOW, que é o bit de start
    }

    // Aguarda meio bit para sincronizar a leitura com o centro dos bits
    _sw_uart_wait_half_T();

    // Variável para armazenar o caractere reconstruído
    char receivedChar = 0;

    // Lê os 8 bits do caractere
    for (int i = 0; i < 8; i++) {
        _sw_uart_wait_half_T(); // Espera o tempo de um bit
        int bit = digitalRead(rxPin); // Lê o estado do pino de recepção
        receivedChar |= (bit << i); // Constrói o caractere bit a bit
    }

    // Lê o bit de paridade
    _sw_uart_wait_half_T();
    int parityBit = digitalRead(rxPin);

    // Verifica o bit de stop (HIGH)
    _sw_uart_wait_half_T();
    if (digitalRead(rxPin) == LOW) {
        Serial.println("Erro: Bit de stop não detectado corretamente!");
        return 0; // Indica que algo deu errado
    }

    // Verifica se a paridade está correta
    int expectedParity = calc_even_parity(receivedChar);
    if (parityBit != expectedParity) {
        Serial.println("Erro de Paridade Detectado!");
        return 0; // Indica que houve um erro de paridade
    }

    return receivedChar; // Retorna o caractere completo
}

void loop() {
    // Lê um caractere e imprime no monitor serial
    char received = readChar();
    if (received != 0) { // Verifica se um caractere foi lido corretamente
        Serial.print("Recebido: ");
        Serial.println(received);
    }
}

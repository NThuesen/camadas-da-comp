int txPin = 3;  // Pino digital para transmissão
int baudRate = 9600;  // Define o baud rate

void setup() {
    pinMode(txPin, OUTPUT); // Configura o pino como saída
    Serial.begin(9600); // Para monitoramento pelo monitor serial do Arduino
}

// Função para substituir o uso delay()
void _sw_uart_wait_half_T() {
    for (int i = 0; i < 1093; i++) {
        asm("NOP");
    }
}

void sendBit(bool bit) {
    digitalWrite(txPin, bit ? HIGH : LOW); // Envia um bit
    _sw_uart_wait_half_T(); // Espera pela duração de um bit
}

// Função para calcular a paridade par (even parity) usando o método do professor
int calc_even_parity(char data) {
    int ones = 0;
    for (int i = 0; i < 8; i++) {
        ones += (data >> i) & 0x01;
    }
    return ones % 2;
}

void sendChar(char c) {
    // 1. Enviar o bit de start (LOW)
    sendBit(LOW);

    // 2. Enviar os 8 bits do caractere
    for (int i = 0; i < 8; i++) {
        bool bit = (c >> i) & 1; // Extrai o i-ésimo bit do caractere
        sendBit(bit);
    }

    // 3. Calcular e enviar o bit de paridade
    int parityBit = calc_even_parity(c);
    sendBit(parityBit);

    // 4. Enviar o bit de stop (HIGH)
    sendBit(HIGH);
}

void loop() {
    char teste = 'A';
    sendChar(teste);
    Serial.println(teste);
    delay(1000);
}

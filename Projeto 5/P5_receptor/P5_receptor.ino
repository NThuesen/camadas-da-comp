const int rxPin = 4;

void setup() {
  pinMode(rxPin, INPUT);  
  Serial.begin(9600);     
}

void loop() {
  char receivedData = receiveByte(); 
  Serial.print("Dado recebido: ");
  Serial.println(receivedData);  
  
}

char receiveByte() {
  char aux = 0;


  while (digitalRead(rxPin) == HIGH);
  

  half_T();  
  wait_T();

  
  for (int i = 0; i < 8; i++) {
    int bitReceived = digitalRead(rxPin);  
    aux |= (bitReceived << i);             
    wait_T();  
  }

 
  int parity = digitalRead(rxPin);
  
  if (parity != calc_even_parity(aux)) {
    //Serial.println("Erro de paridade!");
  } else {
    //Serial.println("Paridade correta.");
  }

  if (digitalRead(rxPin) != HIGH) {
    //Serial.println("Erro: Bit de stop inválido.");
  } else {
    //Serial.println("Bit de stop correto (HIGH).");
  }

  return aux;
}

void half_T() {
  for (int i = 0; i < 150; i++) {
    asm("NOP");
  }
}
void wait_T() {
  for (int i = 0; i < 310; i++) {
    asm("NOP");
  }
}

int calc_even_parity(char data) {
  int ones = 0;
  for (int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }
  return ones % 2;
}
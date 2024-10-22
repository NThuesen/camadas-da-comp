const int txPin = 3;

void setup() {
  pinMode(txPin, OUTPUT);  
  Serial.begin(9600);  
  Serial.println("Transmissor pronto.");
}

int calc_even_parity(char data) {
  int ones = 0;
  for (int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }
  return ones % 2;
}

void wait_T() {
  for (int i = 0; i < 295; i++) {
    asm("NOP");
  }
}

void sendByte(char data) {

  digitalWrite(txPin, LOW);
  wait_T();  

  for (int i = 0; i < 8; i++) {
    int bitToSend = (data >> i) & 1;  
    digitalWrite(txPin, bitToSend);   
    wait_T(); 
  }

  int parity = calc_even_parity(data);

  digitalWrite(txPin, parity);
  wait_T();

  digitalWrite(txPin, HIGH);
  wait_T();
}

void loop() {
  char dataToSend = 'L'; 
  sendByte(dataToSend);
  delay(2);          
}
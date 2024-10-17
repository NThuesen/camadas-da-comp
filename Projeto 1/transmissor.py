from decimal import Decimal
from enlace import *
import struct
import time
from datetime import datetime
import random

serialName = "COM5"  # Atualize para a porta correta no seu computador

def codifica(numero):
    return struct.pack('!f', numero)

def main():
    try:
        print("Iniciou o main no transmissor")

        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.2)

        # Enviando o byte de sacrifício
        com1.sendData(b'\x00')  # Envia um byte de sacrifício
        time.sleep(1)

        print("Abriu a comunicação")

        # Números que você deseja enviar
        numeros = []  # Lista para armazenar os números a enviar
        quantidade_de_numeros = random.randint(5, 15)  # Gera a quantidade de números aleatórios entre 5 e 15

        for i in range(quantidade_de_numeros):
            # Gera um número de ponto flutuante aleatório entre -10^38 e 10^38
            numero = random.uniform(-1 * 10**38, 1 * 10**38)
            numeros.append(numero)
            
        soma_propria = sum(numeros)

        txBuffer = b''

        for numero in numeros:
            txBuffer += codifica(numero)  # Codifica e adiciona ao buffer
            txBuffer += b'\x00\x00\x00\x00'  # Adiciona um separador

        # Adiciona um byte de finalização ao final da transmissão
        finalizacao = codifica(1111)  # Um número especial para indicar final
        txBuffer += finalizacao

        print("Enviando números codificados")
        com1.sendData(txBuffer)

        print(f"Enviou {len(txBuffer)} bytes")

        # time.sleep(2)  # Pequeno atraso para garantir que o receptor tenha tempo de processar

        # Espera pela resposta com timeout
        timeout = 5  # Timeout de 5 segundos
        start_time = datetime.now()

        while True:
            if (datetime.now() - start_time).seconds >= timeout:
                raise Exception("Timeout: Nenhuma resposta recebida do receptor.")
            
            if not com1.rx.getIsEmpty():
                rxBuffer, nRx = com1.getData(4)

                if nRx == 4:
                    soma_recebida = struct.unpack('!f', rxBuffer)[0]
                    print(f"Soma recebida do receptor: {soma_recebida}")
                    if abs(soma_propria - soma_recebida) > soma_propria/100:
                        raise Exception('somas não estão batendo')
                    break  # Saia do loop assim que os dados forem recebidos
                else:
                    print(f"Recebido {nRx} bytes, mas esperava 4")
            time.sleep(0.1)  # Pequeno atraso para não sobrecarregar o loop

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()

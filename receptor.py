import time
import struct
from enlace import enlace

def codifica(numero):
    return struct.pack('!f', numero)

def decodifica(bytes):
    return struct.unpack('!f', bytes)[0]

def main():
    com2 = enlace("COM4")
    com2.enable()

    # Seguindo o modelo do professor para lidar com o byte de sacrifício
    print("Esperando 1 byte de sacrifício...")
    rxBuffer, nRx = com2.getData(1)  # Recebe 1 byte (sacrifício)
    com2.rx.clearBuffer()  # Limpa o buffer de recepção
    time.sleep(.1)  # Pequeno delay para garantir que tudo esteja pronto

    numeros_recebidos = []
    while True:
        rxBuffer, nRx = com2.getData(4)
        if nRx > 0:
            numero = decodifica(rxBuffer)
            numeros_recebidos.append(numero)
            print(f"Número recebido: {numero}")
        else:
            break

    soma = sum(numeros_recebidos)
    com2.sendData(codifica(soma))
    print(f"Soma enviada ao cliente: {soma}")

    com2.disable()

if __name__ == "__main__":
    main()

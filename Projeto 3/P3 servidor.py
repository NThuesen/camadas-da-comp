import numpy as np
from enlace import *
import struct
import time

serialName = "COM4"  

def decodifica(bytes):
    return struct.unpack('b', bytes)[0]

def codifica(numero):
    return struct.pack('b', numero)

def handshake(rxBuffer:bytes):
    com2 = enlace(serialName)
    com2.enable()
    print("Devolvendo o handshake")
    com2.sendData(rxBuffer[1:10])
    return rxBuffer[0]
    
def main():
    try:
        
        print("Iniciou o main no receptor")
        
        com2 = enlace(serialName)
        com2.enable()

        print("esperando 1 byte de sacrifício...")
        rxBuffer, nRx = com2.getData(1)
        com2.rx.clearBuffer()

        print('enviando byte de sacrificio')
        com2.sendData(b'\x00')  # Envia um byte de sacrifício
        com2.rx.clearBuffer()

        print("Aguardando dados...") 
        rxBuffer, nRx = com2.getData(15)
        print("Recebemos {} bytes".format(nRx))
        if(nRx == 15):
            handshake = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            handshake += b'\x10\x10\x10'
            tamanho_payload = int.from_bytes(rxBuffer[7:8],'big')
            tamanho_loop = int.from_bytes(rxBuffer[11:12],'big')
            quantidade_de_pacotes = int.from_bytes(rxBuffer[9:10],'big')
            print("Handshake recebido")
            print(f'esse é o tamanho do loop: {tamanho_loop}')
            com2.sendData(handshake)
            print("Devolvendo Handshake")

        com2.rx.clearBuffer()
        print("Preparado para receber dados")

        #########################################################################################
        payload = b''
        index_do_pacote = 0
        index_anterior = 0
        for i in range(tamanho_loop):
            while True:
                len_rx = com2.rx.getBufferLen()
                confirmando_pacote = True
                if len_rx == 15+tamanho_payload:
                    while confirmando_pacote:
                        rxBuffer, nRx = com2.getData(15+tamanho_payload)
                        tamanho_payload = rxBuffer[3]
                        index_do_pacote = rxBuffer[1]
                        time.sleep(0.2)
                        if index_do_pacote == index_anterior + 1:
                            print('numero do pacote correto!')
                            time.sleep(0.1)
                            if rxBuffer[-3:] == b'\x10\x10\x10':
                                print('eop tambem está correto!')
                                time.sleep(0.1)
                                payload += rxBuffer[12:-3]
                                acknowledge =b'\x01\x02\x03\x04\x05\x06\x00\x00\x00\x00\x00\x00'
                                acknowledge += b'\x10\x10\x10'
                                com2.sendData(acknowledge)
                                com2.rx.clearBuffer()
                                index_anterior += 1
                                confirmando_pacote = False
                            else:
                                com2.rx.clearBuffer()
                                time.sleep(0.1)
                                print('erro no eop, pedindo o reenvio do pacote')
                                reenvio =b'\x12\x11\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                reenvio += b'\x10\x10\x10'
                                com2.sendData(reenvio)
                        else:
                            time.sleep(0.1)
                            com2.rx.clearBuffer()
                            print(f'erro no numero do pacote era esperado {index_anterior+1} e recebemos {index_do_pacote}, pedindo o reenvio do pacote')
                            reenvio =b'\x00\x00\x00\x00\x00\x00\x06\x05\x04\x03\x02\x01'
                            reenvio += b'\x10\x10\x10'
                            com2.sendData(reenvio)

                    print(f'pacote numero {index_do_pacote} armazenado')
                    time.sleep(0.1)
                    pass
                else:
                    'tamanho do payload informado está incorreto, pedindo reenvio do pacote'
                    reenvio =b'\x00\x00\x00\x00\x00\x00\x06\x05\x04\x03\x02\x01'
                    reenvio += b'\x10\x10\x10'
                    com2.sendData(reenvio)

                if index_do_pacote == tamanho_loop:
                    print('rodou todas as vezes o loop')
                    print(f'tamanho do payload (do loop): {len(payload)}')
                    break
            break


        while True:
            len_rx = com2.rx.getBufferLen()
            if len_rx >= 15:
                rxBuffer, nRx = com2.getData(15+tamanho_payload)
                payload += rxBuffer[12:-3]
                index_do_pacote = rxBuffer[1]
                print(f'pacote numero {index_do_pacote} armazenado')
                break
        if index_do_pacote == quantidade_de_pacotes:
            print('recebemos todos os pacotes')
        else:
            raise Exception('Faltaram pacotes ;-;')
        print(f'tamanho do payload (final): {len(payload)}')
        #########################################################################################

        imagew = "./imgs/imageW.png"
        f = open(imagew, 'wb')
        f.write(payload)

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()


    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()


if __name__ == "__main__":
    main()

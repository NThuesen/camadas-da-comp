import numpy as np
from enlace import *
import time


serialName = "COM3"  

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
        # dados = 3
        # ok = 4
        # erro = 5
        
        payload = b''
        index_do_pacote = 0
        index_anterior = 0
        for i in range(tamanho_loop):
            while True:
                time.sleep(0.2)
                len_rx = com2.rx.getBufferLen()
                confirmando_pacote = True
                # print(f'lenrx = {len_rx} e ele deveria ser igual a {15+tamanho_payload}')
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
                                time.sleep(0.1)
                                print('erro no eop, pedindo o reenvio do pacote')
                                reenvio =b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02'
                                reenvio += b'\x10\x10\x10'
                                com2.sendData(reenvio)
                                com2.rx.clearBuffer()
                        else:
                            time.sleep(0.1)
                            print(f'erro no numero do pacote era esperado {index_anterior+1} e recebemos {index_do_pacote}, pedindo o reenvio do pacote')
                            reenvio =b'\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03'
                            reenvio += b'\x10\x10\x10'
                            com2.sendData(reenvio)
                            com2.rx.clearBuffer()
                    print(f'pacote numero {index_do_pacote} armazenado')
                    time.sleep(0.1)
                else:
                    'tamanho do payload informado está incorreto, pedindo reenvio do pacote'
                    reenvio =b'\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04'
                    reenvio += b'\x10\x10\x10'
                    com2.sendData(reenvio)

                if index_do_pacote == tamanho_loop:
                    print('rodou todas as vezes o loop')
                    print(f'tamanho do payload (do loop): {len(payload)}')
                    break
            break
            

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

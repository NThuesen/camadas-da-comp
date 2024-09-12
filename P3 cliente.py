from decimal import Decimal
from enlace import *
import struct
import time
from datetime import datetime
import random

serialName = "COM5"  # Atualize para a porta correta no seu computador

def codifica(numero):
    return struct.pack('B', numero)

def handshake(com1, tamanho_loop, tamanho_payload):
    print('Enviando Handshake')
    txbuffer = b'\x00\x00\x00\x00\x00\x00'
    txbuffer += int.to_bytes(tamanho_payload,2,'big')
    txbuffer += int.to_bytes(tamanho_loop+1,2,'big')
    txbuffer += int.to_bytes(tamanho_loop,2,'big')
    txbuffer += b'\x10\x10\x10'
    com1.sendData(txbuffer)
    pass
    
def enviar_pacote_cheio(image_bytes,index,total_pacotes,tamanho_do_prox,com1):
    txBuffer = b'\x10'  
    #txBuffer += int.to_bytes(index,2,'big') 
    txBuffer += int.to_bytes(index,1,'big') 
    txBuffer += int.to_bytes(total_pacotes,1,'big')   
    txBuffer += int.to_bytes(tamanho_do_prox,1,'big')  
    txBuffer += b'\x00' * 8
    txBuffer += image_bytes
    txBuffer += b'\x10\x10\x10'
    com1.sendData(txBuffer)
    return txBuffer

def enviar_ultimo_pacote(image_bytes,tamanho, index, com1):
    txBuffer = b'\x10'
    txBuffer += int.to_bytes(index,1,'big') 
    txBuffer += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x32'
    txBuffer += image_bytes[:tamanho]
    txBuffer += b'\x10\x10\x10'
    com1.sendData(txBuffer)
    return txBuffer

def main():
    try:
        print("Iniciou o main no transmissor")

        with open('imgs/sol.png', 'rb') as file:
            image_bytes = file.read()
        
        tamanho_img = len(image_bytes)
        resto_loop = tamanho_img % 50
        
        tamanho_loop = int(tamanho_img/50)
        print(f'tamanho da imagem: {tamanho_img}, tamanho do loop: {tamanho_loop}')

        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.2)


        #########################################################################################
        tentando_conectar = True
        Nao_quer_conectar = False
        timeout = 5  # Timeout de 5 segundos
        start_time = datetime.now()
        resposta = ''

        while tentando_conectar:
            if (datetime.now() - start_time).seconds >= timeout:
                print('------------------------------------------')
                resposta = input('Servidor inativo. Tentar novamente? S/N ')
                start_time = datetime.now()
                while True:
                    if resposta != 'S' and resposta != 'N':
                        resposta = input("Digite S (sim) ou N (não): ")
                    else:
                        break
            
            if resposta == 'N':
                tentando_conectar = False
                Nao_quer_conectar = True
                com1.disable()
                break

            print('enviando byte de sacrificio')
            com1.sendData(b'\x00')  # Envia um byte de sacrifício
            time.sleep(1)

            if not com1.rx.getIsEmpty():
                print("esperando 1 byte de sacrifício...")
                rxBuffer, nRx = com1.getData(1)
                com1.rx.clearBuffer()
                time.sleep(0.2)

                print("chamando função handshake")
                handshake(com1,tamanho_loop,50)
                print('esperando resposta')
                time.sleep(0.1)
                rxBuffer, nRx = com1.getData(15)
                if nRx == 15:
                    print('Handshake recebido com sucesso')
                tentando_conectar = False
        
        while not Nao_quer_conectar:
            #########################################################################################

            print('iniciando transmissão de dados')

            #########################################################################################
            payload = b''
            bytes_enviados = 0
            for i in range(tamanho_loop):
                actual_imgBytes = image_bytes[i*50:(i+1)*50]
                bytes_enviados += len(actual_imgBytes)

                if tamanho_img-bytes_enviados>=50:
                    tamanho_prox = 50
                else:
                    tamanho_prox = tamanho_img - bytes_enviados

                numero_pacote = i+1
                print(f"pacote numero {numero_pacote} esta sendo enviado")
                while True:
                    buffer_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )
                    time.sleep(0.1)
                    esperando_confirmar = True
                    while esperando_confirmar:
                        com1.rx.clearBuffer()
                        time.sleep(0.2)
                        resposta_servidor, nrx = com1.getData(15)
                        print('cheguei até aqui')    # não apagar o print, ele magicamente para de funcionar se apagar...
                        print(resposta_servidor[:11]) # não apagar o print, ele magicamente para de funcionar se apagar...
                        if resposta_servidor[:11] == b'\x01\x02\x03\x04\x05\x06\x00\x00\x00\x00\x00':
                            print('pacote enviado com sucesso!')
                            esperando_confirmar = False


                        elif resposta_servidor[:11] ==  b'\x12\x11\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                            print(f'problema no eop, reenviando o pacote numero: {numero_pacote}')
                            buffer_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )   


                        elif resposta_servidor[:11] ==  b'\x12\x11\x10\x09\x08\x07\x06\x05\x04\x01\x02\x03':
                            print(f'problema no tamanho do payload, reenviando o pacote numero: {numero_pacote}')
                            buffer_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )   


                        elif resposta_servidor[:11] == b'\x00\x00\x00\x00\x00\x00\x06\x05\x04\x03\x02\x01':   
                            print(f'problema no numero do pacote, reenviando o pacote numero: {numero_pacote}')
                            buffer_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )   


                        else:
                            com1.rx.clearBuffer()
                    break

                payload += buffer_enviado[12:-3]

            # Fora do loop principal (payloads de 50 bytes)
            print(f'tamanho do payload (do loop): {len(payload)}')

            actual_imgBytes = image_bytes[-resto_loop:]
            print(f'enviando ultimo pacote {tamanho_loop+1}')
            print('--------------------------------------')
            time.sleep(0.2)
            buffer_enviado = enviar_ultimo_pacote(actual_imgBytes,resto_loop, tamanho_loop+1, com1)
            payload += buffer_enviado[12:-3]
            print(f'tamanho do payload (final): {len(payload)}')
            if payload == image_bytes:
                print('enviamos o payload correto')
            else:
                print('temos um problema com o payload')
            break
            
            #########################################################################################

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
    
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()


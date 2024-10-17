from enlace import *
import time
from datetime import datetime
from crc import Calculator, Crc16

serialName = "COM5"  # Atualize para a porta correta no seu computador

calculator = Calculator(Crc16.MODBUS, optimized=True)

# Função para escrever o log em um arquivo txt
def escrever_log(mensagem_log):
    with open('log_cliente.txt', 'a') as arquivo_log:
        arquivo_log.write(mensagem_log + '\n')  # Adiciona a mensagem e quebra de linha


def handshake(com1, tamanho_loop, tamanho_payload):
    print('Enviando Handshake')
    txbuffer = b'\x00\x00\x00\x00\x00\x00'
    txbuffer += int.to_bytes(tamanho_payload,2,'big')
    txbuffer += int.to_bytes(tamanho_loop,2,'big')
    txbuffer += int.to_bytes(tamanho_loop,2,'big')
    txbuffer += b'\x10\x10\x10'
    com1.sendData(txbuffer)
    mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensagem_log += f'/ envio / 4 / {len(txbuffer)}'
    escrever_log(mensagem_log)
    pass
    


def enviar_pacote_cheio(image_bytes, index, total_pacotes, tamanho_do_prox, com1):
    # Calcular o CRC do payload (apenas image_bytes)
    crc = calculator.checksum(image_bytes)

    # Montar o cabeçalho
    txBuffer = b'\x10'
    txBuffer += int.to_bytes(index, 1, 'big')  # Índice do pacote
    txBuffer += int.to_bytes(total_pacotes, 1, 'big')  # Total de pacotes
    txBuffer += int.to_bytes(tamanho_do_prox, 1, 'big')  # Tamanho do próximo pacote
    txBuffer += int.to_bytes(crc, 2, 'big')  # Anexar o CRC no head
    txBuffer += b'\x00' * 6  # Preencher o restante do cabeçalho

    # Anexar o payload (dados)
    txBuffer += image_bytes

    # Anexar o EOP
    txBuffer += b'\x10\x10\x10'

    # Enviar o pacote
    com1.sendData(txBuffer)

    # Retornar o buffer e o CRC calculado
    return txBuffer, crc.to_bytes(2, 'big')

def main():
    try:
        print("Iniciou o main no transmissor")

        with open('imgs/image.png', 'rb') as file:
            image_bytes = file.read()
        
        tamanho_img = len(image_bytes)
        resto_loop = tamanho_img % 50
        
        print(image_bytes)
        tamanho_loop = int(tamanho_img/50) +1
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
                    mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    mensagem_log += f'/ receb / 5 / {nRx}'
                    escrever_log(mensagem_log)
                    print('Handshake recebido com sucesso')
                tentando_conectar = False
        
        while not Nao_quer_conectar:
            #########################################################################################

            print('iniciando transmissão de dados')

            #########################################################################################
            # dados = 3
            # ok = 4
            # erro = 5
            erro_de_ordem = False
            erro_de_crc = False
            bytes_enviados = 0
            i = 0
            while i < tamanho_loop:
                actual_imgBytes = image_bytes[i*50:(i+1)*50]
                bytes_enviados += len(actual_imgBytes)
                print(f'bytes enviados {bytes_enviados}')
                i += 1

                if tamanho_img - bytes_enviados>=50:
                    tamanho_prox = 50
                else:
                    tamanho_prox = tamanho_img - bytes_enviados
                print(f'tamanho prox {tamanho_prox}')
                
                if not erro_de_ordem:
                    i = 2
                    erro_de_ordem = True
                


                numero_pacote = i
                

                print(f"pacote numero {numero_pacote} esta sendo enviado")

                while True: #Loop para verificar o envio do pacote
                    if  numero_pacote == tamanho_loop-1:
                        tamanho_prox = tamanho_img - 50*numero_pacote
                        buffer_enviado, crc_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )
                        

                    elif numero_pacote != tamanho_loop:
                        print(f'numero_pacote do while true = {numero_pacote}')
                        buffer_enviado, crc_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )
                       
                    else:
                        actual_imgBytes = image_bytes[-resto_loop:]
                        print(f'enviando ultimo pacote {tamanho_loop}')
                        print(f'actual [ {actual_imgBytes}]')
                        print('--------------------------------------')
                        time.sleep(0.2)
                        buffer_enviado, crc_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )
                   
                    # print(f'enviamos {buffer_enviado}')
                    
                    # Montar a mensagem de log
                    mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    mensagem_log += f'/ envio / 3 / {len(buffer_enviado)} / {numero_pacote} / {tamanho_loop} / {crc_enviado.hex()}'
                    escrever_log(mensagem_log)

                    time.sleep(0.1)
                    esperando_confirmar = True

                    while esperando_confirmar:
                        # print('chegamos no loop confirmar')
                        com1.rx.clearBuffer()
                        time.sleep(0.2)
                        resposta_servidor, nrx = com1.getData(15)
                        # print('passou o get data')
                        # print(resposta_servidor)
                        
                        # print('loop do confirmar!')    

                        if resposta_servidor[:12] == b'\x01\x02\x03\x04\x05\x06\x00\x00\x00\x00\x00\x00':
                            print('pacote enviado com sucesso!')
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ receb  / 4 / {len(resposta_servidor)}'
                            esperando_confirmar = False

                        elif resposta_servidor[:12] == b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01':
                            print(f'problema no CRC, reenviando o pacote numero: {numero_pacote}')
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ receb  / 5 / {len(resposta_servidor)}'
                            escrever_log(mensagem_log)                        
                            buffer_enviado, crc_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ envio / 3 / {len(buffer_enviado)} / {numero_pacote} / {tamanho_loop} / {crc_enviado.hex()}'

                        elif resposta_servidor[:12] ==  b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02':
                            print(f'problema no eop, reenviando o pacote numero: {numero_pacote}')
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ receb  / 5 / {len(resposta_servidor)}'
                            escrever_log(mensagem_log)
                            buffer_enviado, crc_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ envio / 3 / {len(buffer_enviado)} / {numero_pacote} / {tamanho_loop} / {crc_enviado.hex()}'

                        elif resposta_servidor[:12] ==  b'\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04':
                            print(f'problema no tamanho do payload, reenviando o pacote numero: {numero_pacote}')
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ receb  / 5 / {len(resposta_servidor)}'
                            escrever_log(mensagem_log)
                            buffer_enviado, crc_enviado = enviar_pacote_cheio(actual_imgBytes, index=numero_pacote , total_pacotes= tamanho_loop, tamanho_do_prox= tamanho_prox, com1= com1 )
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ envio / 3 / {len(buffer_enviado)} / {numero_pacote} / {tamanho_loop} / {crc_enviado.hex()}'

                        elif resposta_servidor[:11] == b'\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03':  
                            # print(resposta_servidor)
                            # print(resposta_servidor[11:12]) 
                            i = int.from_bytes(resposta_servidor[11:12], 'big')
                            numero_pacote = i
                            print(f'problema no numero do pacote, reenviando o pacote numero: {i}')
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ receb  / 5 / {len(resposta_servidor)}'
                            escrever_log(mensagem_log)
                            print('alterando o index para menos 1')
                            actual_imgBytes = image_bytes[(i-1)*50:(i)*50]

                            buffer_enviado, crc_enviado = enviar_pacote_cheio(actual_imgBytes, index=i, total_pacotes=tamanho_loop, tamanho_do_prox=tamanho_prox, com1=com1)
                            
                            mensagem_log = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            mensagem_log += f'/ envio / 3 / {len(buffer_enviado)} / {i} / {tamanho_loop} / {crc_enviado.hex()}'

                        else:
                            com1.rx.clearBuffer()
                        escrever_log(mensagem_log)
                    break
                
            break
            
            #########################################################################################

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


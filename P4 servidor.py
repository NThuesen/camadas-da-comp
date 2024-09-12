import numpy as np
from enlace import *
import struct
import time

serialName = "COM4"  

# Função para calcular CRC-16
def calcular_crc(payload: bytes):
    crc = 0xFFFF
    for byte in payload:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

# Função para escrever no log
def log_evento_servidor(instante, acao, tipo_mensagem, tamanho, pacote_numero=None, total_pacotes=None, crc=None):
    with open('log_servidor.txt', 'a') as log:
        log.write(f"{instante} / {acao} / {tipo_mensagem} / {tamanho} bytes / ")
        if pacote_numero is not None and total_pacotes is not None:
            log.write(f"{pacote_numero} / {total_pacotes} / {hex(crc)}")
        log.write("\n")

def handshake(rxBuffer:bytes):
    com2 = enlace(serialName)
    com2.enable()
    print("Devolvendo o handshake")
    com2.sendData(rxBuffer[1:10])
    return rxBuffer[0]

# Função principal
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
        print(f"Recebemos {nRx} bytes")
        
        if nRx == 15:
            handshake = b'\x00' * 12 + b'\x10\x10\x10'
            tamanho_payload = int.from_bytes(rxBuffer[7:8], 'big')
            tamanho_loop = int.from_bytes(rxBuffer[11:12], 'big')
            quantidade_de_pacotes = int.from_bytes(rxBuffer[9:10], 'big')
            print("Handshake recebido")
            print(f'Tamanho do loop: {tamanho_loop}')
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
                if len_rx == 15 + tamanho_payload:
                    while confirmando_pacote:
                        rxBuffer, nRx = com2.getData(15 + tamanho_payload)
                        tamanho_payload = rxBuffer[3]
                        index_do_pacote = rxBuffer[1]

                        # Verificando o CRC
                        payload_recebido = rxBuffer[12:-3]
                        crc_recebido = int.from_bytes(rxBuffer[-5:-3], 'big')
                        crc_calculado = calcular_crc(payload_recebido)

                        time.sleep(0.2)
                        if index_do_pacote == index_anterior + 1:
                            print('Número do pacote correto!')
                            time.sleep(0.1)
                            if rxBuffer[-3:] == b'\x10\x10\x10':
                                print('EOP também está correto!')
                                
                                if crc_calculado == crc_recebido:
                                    print('CRC válido!')
                                    
                                    # Registro do log (recepção do pacote com sucesso)
                                    instante_receb = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
                                    log_evento_servidor(instante_receb, "receb", "dados", nRx, i+1, tamanho_loop, crc_calculado)

                                    # Enviando acknowledgment
                                    acknowledge = b'\x01' * 15  # Exemplo de mensagem de ACK
                                    com2.sendData(acknowledge)

                                    # Registro do log (envio de confirmação)
                                    instante_envio = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
                                    log_evento_servidor(instante_envio, "envio", "ok", len(acknowledge), i+1, tamanho_loop, None)

                                    com2.rx.clearBuffer()
                                    index_anterior += 1
                                    confirmando_pacote = False
                                    payload += payload_recebido
                                else:
                                    print('Erro de CRC, pedindo reenvio do pacote')
                                    reenvio = b'\x00' * 15  # Exemplo de mensagem de erro CRC
                                    com2.sendData(reenvio)
                                    # Registro do log (envio de erro CRC)
                                    instante_envio = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
                                    log_evento_servidor(instante_envio, "envio", "erro", len(reenvio), i+1, tamanho_loop, crc_calculado)
                            else:
                                com2.rx.clearBuffer()
                                time.sleep(0.1)
                                print('Erro no EOP, pedindo reenvio do pacote')
                                reenvio = b'\x12' * 15  # Exemplo de mensagem de erro EOP
                                com2.sendData(reenvio)
                        else:
                            time.sleep(0.1)
                            com2.rx.clearBuffer()
                            print(f'Erro no número do pacote. Esperado {index_anterior+1}, mas recebido {index_do_pacote}. Pedindo reenvio do pacote.')
                            reenvio = b'\x00' * 15  # Exemplo de mensagem de erro no número do pacote
                            com2.sendData(reenvio)

                    print(f'Pacote número {index_do_pacote} armazenado')
                    time.sleep(0.1)
                    pass
                else:
                    'Tamanho do payload informado está incorreto, pedindo reenvio do pacote'
                    reenvio = b'\x12' * 15  # Exemplo de mensagem de erro de tamanho de payload
                    com2.sendData(reenvio)

        # Verificando se recebemos todos os pacotes
        if index_do_pacote == quantidade_de_pacotes:
            print('Recebemos todos os pacotes')
        else:
            raise Exception('Faltaram pacotes ;-;')

        # Registro final do tamanho do payload
        print(f'Tamanho do payload (final): {len(payload)}')

        # Salvando a imagem recebida
        imagew = "./imgs/imageW.png"
        with open(imagew, 'wb') as f:
            f.write(payload)

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()


if __name__ == "__main__":
    main()

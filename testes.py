# import struct

# def enviar_pacote_cheio(image_bytes, index, total_pacotes):
#     txBuffer = b'\x10'  
#     txBuffer += int.to_bytes(index,1,'big') 
#     txBuffer += int.to_bytes(total_pacotes,1,'big')   
#     txBuffer += b'\x00' * 8
#     txBuffer += image_bytes[:50]
#     print(txBuffer[0])
 
#     txBuffer += b'\x10\x10\x10'

#     return txBuffer 
# with open('imgs/sol.png', 'rb') as file:
#     image_bytes = file.read()
 
# tamanho_img = len(image_bytes)
# total_pacotes = (tamanho_img // 50) + (1 if tamanho_img % 50 != 0 else 0)   

# for i in range(total_pacotes):
#     if i < total_pacotes - 1:
#         actual_imgBytes = image_bytes[i*50:(i+1)*50]  
#     else:
#         actual_imgBytes = image_bytes[i*50:]  
#     print(enviar_pacote_cheio(actual_imgBytes, i, total_pacotes))
#     print('------------------------')

def handshake():
    print('Enviando Handshake')
    txbuffer = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    txbuffer += b'\x10\x10\x10'
    return txbuffer

a = handshake()
print(a[:12])
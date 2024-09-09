import struct
def codifica(numero):
    return struct.pack('B', numero)
print(codifica(230))

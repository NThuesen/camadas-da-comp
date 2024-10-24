
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft, fftshift

#funções caso queriram usar para sair...
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)


#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

#####################################################################################
# Funções Fourier
def generateSin(freq, time, fs):
    n = time*fs #numero de pontos
    x = np.linspace(0.0, time, n)  # eixo do tempo
    s = np.sin(freq*x*2*np.pi)
    plt.figure()
    plt.plot(x,s)
    return (x, s)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    #y  = np.append(signal, np.zeros(len(signal)*fs))
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
    yf = fft(signal)
    return(xf, fftshift(yf))
#####################################################################################
# Função para devolver frequencias dependendo da tecla
def TabelaDTFM(tecla):
    if tecla == 1:
        f1 = 697
        f2 = 1209
    elif tecla == 2:
        f1 = 697
        f2 = 1336
    elif tecla == 3:
        f1 = 697
        f2 = 1477
    elif tecla == 4:
        f1 = 770
        f2 = 1209
    elif tecla == 5:
        f1 = 770
        f2 = 1336
    elif tecla == 6:
        f1 = 770
        f2 = 1477
    elif tecla == 7:
        f1 = 852
        f2 = 1209
    elif tecla == 8:
        f1 = 852
        f2 = 1336
    elif tecla == 9:
        f1 = 852
        f2 = 1477
    elif tecla == 0:
        f1 = 941
        f2 = 1336
    return f1, f2

#####################################################################################
# propriedade dos sinais
fs  = 200   # pontos por segundo (frequência de amostragem)
A   = 1   # Amplitude
F   = 1     # Hz
T   = 4     # Tempo em que o seno será gerado
t   = np.linspace(-T/2,T/2,T*fs)

def main():
    
   
    #********************************************instruções*********************************************** 
    # Seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada, conforme tabela DTMF.
    # Então, inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF.
    # De posse das duas frequeências, agora voce tem que gerar, por alguns segundos suficientes para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada.
    # Essas senoides têm que ter taxa de amostragem de 44100 amostras por segundo, sendo assim, voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t).
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as duas senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Você pode gravar o som com seu celular ou qualquer outro microfone para o lado receptor decodificar depois. Ou reproduzir enquanto o receptor já capta e decodifica.
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado, como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    
    print("Inicializando encoder")
    print("Aguardando usuário")
    tecla = int(input("Digite um numero (0 a 9): "))
    f1, f2 = TabelaDTFM(tecla)
    

    # print("Gerando Tons base")
    # print("Executando as senoides (emitindo o som)")
    # print("Gerando Tom referente ao símbolo : {}".format(NUM))
    # sd.play(tone, fs)
    # # aguarda fim do audio
    # sd.wait()
    
    # plotFFT(self, signal, fs)
    # # Exibe gráficos
    # plt.show()
    

if __name__ == "__main__":
    main()

#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft, fftshift

#funções caso queriram usar para sair...
# def signal_handler(signal, frame):
#         print('You pressed Ctrl+C!')
#         sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10 * np.log10(s)
    return(sdB)

def generateSin(freq, time, fs):
    n = time * fs  # numero de pontos
    x = np.linspace(0.0, time, n)  # eixo do tempo
    s = np.sin(freq * x * 2 * np.pi)
    # plt.figure()
    # plt.plot(x,s)
    return (x, s)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    # y  = np.append(signal, np.zeros(len(signal)*fs))
    N = len(signal)
    T = 1 / fs
    xf = np.linspace(-1.0 / (2.0 * T), 1.0 / (2.0 * T), N)
    yf = fft(signal)
    return(xf, fftshift(yf))

dtmf_frequencies = {
    '1': (679, 1209),
    '2': (679, 1336),
    '3': (679, 1477),
    '4': (770, 1209),
    '5': (770, 1336),
    '6': (770, 1477),
    '7': (825, 1209),
    '8': (825, 1336),
    '9': (825, 1477),
    '0': (941, 1336),
    '*': (941, 1209),
    '#': (941, 1477),
    'A': (679, 1633),
    'B': (770, 1633),
    'C': (825, 1633),
    'D': (941, 1633),
}

def take_frequence(tecla):
    freq = dtmf_frequencies[str(tecla)]
    return freq

def main():
    #*instruções**********************************************
    # Seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada, conforme tabela DTMF. OK
    # Então, inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF. OK
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
    tecla = input("Insira uma do teclado numérico DTMF: ")
    while tecla not in dtmf_frequencies.keys():
        tecla = input("Insira uma do teclado numérico DTMF: ")
    frequencias = take_frequence(tecla)
    print(f' Frequências desejadas: {frequencias}')
    fs = 44100  # pontos por segundo (frequência de amostragem)
    T = 4  # Tempo em que o seno será gerado
    t = np.linspace(-T/2, T/2, T*fs)
    sinais = []
    for frequencia in frequencias:
        x, y = generateSin(frequencia, T, fs)

        sinais.append(y)

    senos_somados = sinais[0] + sinais[1]
    plt.figure(figsize=(10, 4))
    plt.plot(t[:1000], senos_somados[:1000])
    plt.title(f'Sinais somados')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')

    tone = senos_somados
    xf , yf = calcFFT(tone,fs)
    print(xf, "X")
    print (yf, "Y")
    sd.play(tone, fs)
    sd.wait()  # aguarda fim do audio

    # plotFFT(self, signal, fs)
    # # Exibe gráficos
    # plt.show()
    plt.figure(figsize=(10, 4))
    plt.stem(xf,abs(yf))
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(tecla))
    plt.show()

if __name__ == "__main__":
    main()


#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

#funções caso queriram usar para sair...
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

dtmf_frequencies = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}

def gerar_sinal_dtmf(tecla, duration=1.0, fs=44100):
    # Frequências das senoides para a tecla
    f1, f2 = dtmf_frequencies[tecla]
    
    # Vetor de tempo
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Geração das senoides
    senoide1 = np.sin(2 * np.pi * f1 * t)
    senoide2 = np.sin(2 * np.pi * f2 * t)
    
    # Sinal final é a soma das duas senoides
    sinal = senoide1 + senoide2
    
    return sinal, t

def plotar_sinal(t, sinal, fs):
    # Plotando o sinal no domínio do tempo
    plt.figure()
    plt.plot(t[:1000], sinal[:1000])  # Mostra apenas os primeiros 1000 pontos
    plt.title('Sinal DTMF no Domínio do Tempo')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Amplitude')
    plt.show()

    # Plotando o sinal no domínio da frequência
    plt.figure()
    plt.magnitude_spectrum(sinal, Fs=fs)
    plt.title('Sinal DTMF no Domínio da Frequência')
    plt.xlabel('Frequência [Hz]')
    plt.ylabel('Magnitude')
    plt.show()


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
    tecla = input("Digite um número de 0 a 9, * ou #: ")

    print("Tecla digitada: {}".format(tecla))

    sinal, t = gerar_sinal_dtmf(str(tecla), duration=3)

    print("Gerando Tons base")
    print("Sinal gerado com sucesso")

    print("Executando as senoides (emitindo o som)")

    fs = 44100
    sd.play(sinal, fs)
    # aguarda fim do audio
    sd.wait()
    
    plotar_sinal(t, sinal, fs)
    # plotFFT(self, signal, fs)
    # Exibe gráficos
    plt.show()
    

if __name__ == "__main__":
    main()

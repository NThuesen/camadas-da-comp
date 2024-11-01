import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft, fftfreq
import time

def filtro_passa_baixa(x, a1, a2, b0, b1, b2):
    """
    Implementa um filtro passa-baixa de segunda ordem usando a equação a diferenças.
    
    Parâmetros:
    x : array
        Sinal de entrada.
    a1, a2 : float
        Coeficientes do denominador (do MATLAB).
    b0, b1, b2 : float
        Coeficientes do numerador (do MATLAB).
    
    Retorna:
    y : array
        Sinal filtrado.
    """
    N = len(x)
    y = np.zeros(N)
    x_n1, x_n2 = 0.0, 0.0  # Amostras anteriores de entrada
    y_n1, y_n2 = 0.0, 0.0  # Amostras anteriores de saída

    for n in range(N):
        y[n] = (-a1 * y_n1) - (a2 * y_n2) + (b0 * x[n]) + (b1 * x_n1) + (b2 * x_n2)

        # Atualizar as amostras anteriores
        y_n2 = y_n1
        y_n1 = y[n]
        x_n2 = x_n1
        x_n1 = x[n]

    return y

def plot_fft(signal, fs, title):
    N = len(signal)
    T = 1.0 / fs
    yf = fft(signal)
    xf = fftfreq(N, T)[:N//2]
    plt.figure()
    plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    plt.title(title)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude')
    plt.grid()
    plt.show()

def main():
    # Parâmetros
    fs = 44100  # Frequência de amostragem
    duration = 4  # Duração da gravação em segundos

    # Coeficientes obtidos do MATLAB
    # Substitua os valores abaixo pelos coeficientes que você anotou do MATLAB
    b0 = 0.0046  # num_z[0]
    b1 = 0.0092  # num_z[1]
    b2 = 0.0046  # num_z[2]
    a1 = -1.7994 # den_z[1]
    a2 = 0.8178  # den_z[2]

    # Capturar o áudio
    print("A gravação começará em 3 segundos")
    time.sleep(3)
    print("Gravação iniciada")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Gravação finalizada")
    dados = audio.flatten()

    # Aplicar o filtro
    y = filtro_passa_baixa(dados, a1, a2, b0, b1, b2)

    # Mostrar FFT antes e depois
    plot_fft(dados, fs, 'Espectro do Sinal Original')
    plot_fft(y, fs, 'Espectro do Sinal Filtrado')

    # Ouvir o sinal filtrado
    print("Reproduzindo o sinal filtrado...")
    sd.play(y, fs)
    sd.wait()

if __name__ == "__main__":
    main()

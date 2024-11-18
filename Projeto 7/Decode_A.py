import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft, fftfreq
import time
from suaBibSignal import signalMeu


def main():
    # Parâmetros
    signal = signalMeu()

    fs = 44100  # Frequência de amostragem
    duration = 4  # Duração da gravação em segundos

    # Coeficientes obtidos do MATLAB
    a = 0.05345
    b = 0.04517
    d = -1.506
    e = 0.6043

    # Capturar o áudio
    print("A gravação começará em 1 segundos")
    time.sleep(1)
    print("Gravação iniciada")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Gravação finalizada")
    audio = audio.flatten()

    saida = [0, 0]
    for i in range(len(audio)):
        if i < 2:
            saida[i] = audio[i]
        else:
            saida.append(-d * saida[i-1] - e * saida[i-2] + a * audio[i-1] + b*audio[i-2])

    # Plotar o áudio original e o áudio filtrado
    signal.plotFFT(saida, fs)
    plt.title("Fourier depois do filtro")

    signal.plotFFT(audio, fs)
    plt.title("Fourier antes do filtro")

    plt.show()

if __name__ == "__main__":
    main()

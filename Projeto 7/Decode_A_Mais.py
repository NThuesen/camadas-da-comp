import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.signal import butter, filtfilt
import time
from suaBibSignal import signalMeu

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs  
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def filtrar_sinal(x, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, x)
    return y

def main():

    signal = signalMeu()


    fs = 44100  # Frequência de amostragem
    cutoff = 1000  # Frequência de corte
    order = 5
    duration = 4  # Duração em segundos

    # Gravar áudio
    print("A gravação começará em 1 segundos")
    time.sleep(1)
    print("Gravação iniciada")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Gravação finalizada")
    x = audio.flatten()

    # Aplicar o filtro de ordem superior
    y = filtrar_sinal(x, cutoff, fs, order=order)

    # Plotar FFT antes e depois da filtragem
    signal.plotFFT(x, fs)
    plt.title("Fourier antes do filtro")

    signal.plotFFT(y, fs)
    plt.title("Fourier depois do filtro")

    

    plt.show()



if __name__ == "__main__":
    main()

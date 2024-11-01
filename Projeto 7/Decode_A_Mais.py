import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.signal import butter, filtfilt
from scipy.fftpack import fft, fftfreq
import time

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs  # Frequência de Nyquist
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def filtrar_sinal(x, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, x)
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
    cutoff = 1000  # Frequência de corte
    order = 5
    duration = 4  # Duração em segundos

    # Gravar áudio
    print("A gravação começará em 3 segundos")
    time.sleep(3)
    print("Gravação iniciada")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Gravação finalizada")
    x = audio.flatten()

    # Aplicar o filtro de ordem superior
    y = filtrar_sinal(x, cutoff, fs, order=order)

    # Plotar FFT antes e depois da filtragem
    plot_fft(x, fs, 'Espectro do Sinal Original')
    plot_fft(y, fs, f'Espectro do Sinal Filtrado (Ordem {order})')

    # Reproduzir o sinal filtrado
    print("Reproduzindo o sinal filtrado (Ordem Superior)...")
    sd.play(y, fs)
    sd.wait()

if __name__ == "__main__":
    main()

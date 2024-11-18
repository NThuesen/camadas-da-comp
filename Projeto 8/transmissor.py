from scipy.io import wavfile
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from suaBibSignal import signalMeu
import sounddevice as sd
import time


# Carrega o arquivo de áudio
samplerate, data = wavfile.read('teste.wav')
print("Samplerate: ", samplerate)
audio = data[:, 0]
lista_tempo = np.arange(0, len(audio)/samplerate, 1/samplerate)

# Filtro passa-baixa

def butter_lowpass(f_corte, fs, order=5):
    return butter(order, f_corte, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, f_corte, fs, order=5):
    b, a = butter_lowpass(f_corte, fs, order=order)
    y = lfilter(b, a, data)
    return y

audio_filtrado = butter_lowpass_filter(audio, 3000, samplerate, 2)

# Gerar grafico para visualização

plt.plot(lista_tempo, audio)
plt.title('Áudio Original')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.show()

plt.plot(lista_tempo, audio_filtrado)
plt.title('Áudio Filtrado')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.show()

#Fourier

signal = signalMeu()
xf, yf = signal.calcFFT(audio, samplerate)

plt.plot(xf, yf)
plt.title('Fourier do Áudio Original')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.show()

xf2, yf2 = signal.calcFFT(audio_filtrado, samplerate)
plt.plot(xf2, yf2)
plt.title('Fourier do Áudio Filtrado')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.show()

# Tocar o som filtrado

wavfile.write('audio/audio_diddy_filtrado.wav', samplerate, audio_filtrado.astype(np.int16))

# Modulando a funcao

def modula(audio, fc, lista_tempo):
    audio_modulado = audio * np.cos(2*np.pi*fc*lista_tempo)
    return audio_modulado

audio_modulado = modula(audio_filtrado, 14000, lista_tempo)

# Plotando audio modulado

plt.plot(lista_tempo, audio_modulado)
plt.title('Áudio Modulado')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.show()

# Fourier do audio modulado

xf3, yf3 = signal.calcFFT(audio_modulado, samplerate)
plt.plot(xf3, yf3)
plt.title('Fourier do Áudio Modulado')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.show()

# Salvando o audio modulado
wavfile.write('audio/audio_diddy_modulado.wav', samplerate, audio_modulado.astype(np.int16))

# Normalizando o audio modulado
audio_modulado_normalizado = audio_modulado / max(abs(audio_modulado))
wavfile.write('audio/audio_diddy_modulado_normalizado.wav', samplerate, audio_modulado_normalizado.astype(np.int16))

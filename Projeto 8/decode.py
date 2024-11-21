from scipy.io import wavfile
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from suaBibSignal import signalMeu
import sounddevice as sd
import time

#Pegando o audio modulado
samplerate, audio_modulado = wavfile.read('teste_modulado.wav')
print("Samplerate: ", samplerate)
lista_tempo = np.arange(0, len(audio_modulado)/samplerate, 1/samplerate)

#Funções de filtro passa-baixa
def butter_lowpass(f_corte, fs, order=5):
    return butter(order, f_corte, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, f_corte, fs, order=5):
    b, a = butter_lowpass(f_corte, fs, order=order)
    y = lfilter(b, a, data)
    return y

#Função de demodulação
def demodula(audio, fc, lista_tempo):
    audio_demodulado = audio * np.cos(2*np.pi*fc*lista_tempo)
    return audio_demodulado

#Audio demodulado
audio_demodulado = demodula(audio_modulado, 14000, lista_tempo)

#Grafico de tempo do audio demodulado
plt.plot(lista_tempo, audio_demodulado)
plt.title('Áudio Modulado')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.show()

#Fourier do audio demodulado

signal = signalMeu()
xf, yf = signal.calcFFT(audio_demodulado, samplerate)

plt.plot(xf, yf)
plt.title('Fourier do Áudio demodulado')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.show()

#Filtrando o audio demodulado
audio_demodulado_filtrado = butter_lowpass_filter(audio_demodulado, 3000, samplerate, 2)

# Salvando o audio demodulado filtrado
wavfile.write('teste_demodulado_filtrado.wav', samplerate, audio_demodulado_filtrado.astype(np.int16))

#Grafico de Fourier do audio demodulado filtrado

xf2, yf2 = signal.calcFFT(audio_demodulado_filtrado, samplerate)

plt.plot(xf2, yf2)
plt.title('Fourier do Áudio demodulado filtrado')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.show()


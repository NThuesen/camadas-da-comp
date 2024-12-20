
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window



class signalMeu:
    def __init__(self):
        self.init = 0

    def __init__(self):
        self.init = 0

 
    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        W = window.hamming(N)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal*W)
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs):
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title('Fourier')

    def filtro_passa_baixa(self, signal,a,b,d,e):
        y = np.zeros_like(signal)
        y[0] = signal[0]
        y[1] = signal[1]
        
        for k in range(2, len(signal)):
            y[k] = - d*y[k-1] - e*y[k-2] + a*signal[k-1] + b*signal[k-2]
        return y


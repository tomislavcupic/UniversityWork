import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import *
from scipy import signal
import pywt
from scipy import io

kobas_iz_matlaba=io.loadmat("C:/Users/Admin/Desktop/tomislav/fer/5. semestar/obrada informacija/Lab1/3_OIkobas.mat")
print(kobas_iz_matlaba)
kobas = kobas_iz_matlaba["kobas"]
kobas = np.squeeze(kobas)
#Prints the data

#Printing some statistics

print(f"broj dana: {len(kobas)}")
print(f"srednja vrijednost vodostaja: {np.mean(kobas)}")
print(f"standardna devijacija: {np.std(kobas)}")
print(f"minimalna vrijednost vodostaja: {np.min(kobas)}")
print(f"maksimalna vrijednost vodostaja: {np.max(kobas)}")
print(f"median vodostaja {np.median(kobas)}")

#Graph of water level
plt.figure(figsize=(40,7))
plt.plot(kobas)
plt.xlabel('godine')
plt.ylabel('razina vode, cm')
plt.xticks(np.arange(0, kobas.size, 365), np.arange(1982,2009,1))
plt.xlim(0, kobas.size)
plt.show()

#Discrete fourier transform
DFT_kobas = fft(kobas)
print(f"vrijednosti: {DFT_kobas}")
plt.figure(figsize=(40,7))
plt.plot(abs(DFT_kobas))
plt.xlabel('k')
plt.ylabel('|X(k)|')
plt.xticks(np.arange(0, kobas.size, 365), np.arange(1982,2009,1))
plt.show()



#Fourier on the time slot
fs = 365
window = 'boxcar'
f,t,Zxx = signal.stft(kobas, fs, window, nperseg=2*365)
plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=np.abs(Zxx.max())/10, shading='gouraud')
plt.colorbar()
plt.title('STFT amplituda')
plt.ylabel('frekvencija k')
plt.xlabel('vrijeme, [godine]')
plt.show()

#I had to change the opening width
fs = 365
window = 'boxcar'
f,t,Zxx = signal.stft(kobas, fs, window, nperseg=365/12)
plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=np.abs(Zxx.max())/10, shading='gouraud')
plt.colorbar()
plt.title('STFT amplituda')
plt.ylabel('frekvencija k')
plt.xlabel('vrijeme, [godine]')
plt.show()

#2 functions of continuous valves
print(pywt.wavelist(kind='continuous'))
valic1 = 'morl'
valic2 = 'mexh'
T = 365
w1 = pywt.ContinuousWavelet(valic1)
plt.figure(1,[50,10])
plt.subplot(1,2,1)
psi, t = w1.wavefun(level = 10)
plt.plot(t, psi)
plt.title("običan morlet")
w2 = pywt.ContinuousWavelet(valic2)
plt.subplot(1,2,2)
psi, t = w2.wavefun(level = 10)
plt.plot(t, psi)
plt.title("mexican hat (sombrero)")
plt.show()


#Using Morlet wavelet draw continuous valence transformation
valic1 = 'morl'
T = 365
w1 = pywt.ContinuousWavelet(valic1)
psi, t = w1.wavefun(level = 10)
step = 0.7
skala = np.arange(0.1,2*T,step)
coef, freqs = pywt.cwt(kobas, skala, valic1)
plt.matshow(abs(coef))
plt.xticks(np.arange(0, kobas.size, 365), np.arange(1982, 2009,1))
plt.yticks([T//12, T//4, T//2, T])
plt.title('morlet valic')
plt.show()

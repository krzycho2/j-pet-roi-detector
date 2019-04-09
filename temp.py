import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib
from lib import VolumeData, vol2Img3D, arr2img
from scipy.signal import argrelmin
from scipy.optimize import curve_fit

def gauss(x, amp, cen, wid):
    return amp * np.exp(-(x-cen)**2 / wid)
# Tutaj sprawdzimy, czy da się przybliżyć histogram sumą krzywych gaussa- rozłożyć na składowe gaussowskie
FantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'
dataFilePath = FantomPath + '/data.pckl'

# 1. Wczytanie danych
fantomVolume = VolumeData(dataFilePath)
# fantomVolume.showAllSlicesInOne()     # Prezentacja wszystkich przekrojów obok siebie
sliceNum = 16
slice2d = fantomVolume.getSlice(sliceNum)

# 2.Znalezienia=e pierwszego minimum na mocno wygładzonym histogramie
binsCount = 1000
bins = np.arange(0, 1, 1/binsCount)
hist = np.histogram(slice2d, bins=bins)[0]

# ind0 = int(0.1*binsCount)
# hist = hist[ind0:]

x = np.linspace(0, 1, len(hist))    # Nie uwzględniony punkt 0

# Wygładzenie histogramu
dlug_okna = int(0.4*binsCount)
hist_mean = np.convolve(hist, np.ones((dlug_okna,))/dlug_okna, mode='valid')
xx = np.linspace(0, 1, len(hist_mean))


mins = np.array(argrelmin(hist_mean)[0]) 
indx = mins[0]
hist = hist[indx:]      # Nowy histogram

# 3. Kolejny histogram i wygłądzanie
hist = np.histogram(slice2d, bins=bins)[0]
hist = hist[indx:]      # Nowy histogram

dlug_okna = int(0.1*binsCount)
hist_mean = np.convolve(hist, np.ones((dlug_okna,))/dlug_okna, mode='valid')
xx = np.linspace(xx[9], 1, len(hist_mean))

# plt.plot(xx, hist_mean, 'b', xx[mins], hist_mean[mins], 'ro')
# plt.yscale('log')

# plt.plot(xx, hist_mean)
# plt.yscale('log')
# plt.show()

tempHist = hist_mean
maxHist = 1
count = 0
while maxHist > 1e-4:
    init_params = [1, 0, 1]     # [amp, cen, wid]
    params, covar = curve_fit(gauss, xx, tempHist, p0=init_params)
    plt.plot(xx, tempHist, 'b', xx, gauss(xx, params[0], params[1], params[2]), 'r')
    # plt.yscale('log')
    plt.title('Iteracja: ' + str(count))
    plt.show()
    tempHist = tempHist - gauss(xx, params[0], params[1], params[2])
    plt.plot(xx,tempHist)
    plt.show()
    maxHist = max(tempHist)
    count +=1

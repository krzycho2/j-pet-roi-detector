# Segmentacja z wykorzystaniem algorytmów progujących:
# - binarnych
# - Otsu
# - Addaptacyjnego

from lib import VolumeData
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from skimage import exposure, filters
import cv2

# Wczytywanie obrazu
FantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'
dataFilePath = FantomPath + '/data.pckl'
fantomVolume = VolumeData(dataFilePath)
sliceNum = 16
slice2d = fantomVolume.getSlice(sliceNum)
slice2d_u8 = np.array(255*slice2d, dtype='uint8')

# open cv - WSZYTKIE METODY
path = FantomPath + '/fantom_18_slice.png'
# Zwykłe
ret1, th1 = cv2.threshold(slice2d_u8, 127, 255, cv2.THRESH_BINARY)
# Otsu
ret2, th2 = cv2.threshold(slice2d_u8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Adaptive-  Mean
th3 = cv2.adaptiveThreshold(slice2d_u8, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,21,2)
# Adaptive - Gaussian
th4 = cv2.adaptiveThreshold(slice2d_u8, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,21,2)

plt.subplot(2,2,1)
plt.imshow(th2*slice2d_u8)
plt.title('Progowanie Otsu')
plt.subplot(2,2,2)
plt.imshow(th1*slice2d_u8)
plt.title('Progowanie zwykłe')
plt.subplot(2,2,3)
plt.imshow(th3*slice2d_u8)
plt.title('Progowanie adaptacyjne - MEAN')
plt.subplot(2,2,4)
plt.imshow(th4*slice2d_u8)
plt.title('Progowania adaptacyjne - GAUSSIAN')
plt.show()



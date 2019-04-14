# Segmentacja z wykorzystaniem algorytmów progujących:
# - binarnych
# - Otsu
# - Addaptacyjnegos

from lib import VolumeData
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from skimage import exposure, filters
from skimage.morphology import disk
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
ret1, mask1 = cv2.threshold(slice2d_u8, 127, 255, cv2.THRESH_BINARY)
# Otsu
ret2, mask2 = cv2.threshold(slice2d_u8, 0, 255,cv2.THRESH_OTSU)
# Adaptive-  Mean
mask3 = cv2.adaptiveThreshold(slice2d_u8, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,21,2)
# Adaptive - Gaussian
mask4 = cv2.adaptiveThreshold(slice2d_u8, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,21,2)

plt.imshow(slice2d_u8)
plt.title('Obraz oryginalny')
plt.show()
plt.imshow(mask1)
plt.title('Segmentacja obrazu przy pomocu progowania zwykłego')
plt.show()
plt.imshow(mask2)
plt.title('Segmentacja obrazu przy pomocy progowania Otsu')
plt.show()
plt.imshow(mask3)
plt.title('Segmentacja obrazu przy pomocy progowania adaptacyjnego')
plt.show()




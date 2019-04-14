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


# Adaptive-  Mean
mask3 = cv2.adaptiveThreshold(slice2d_u8, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,7,0)
# # Adaptive - Gaussian
# mask4 = cv2.adaptiveThreshold(slice2d_u8, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv2.THRESH_BINARY,7,2)
# plt.subplot(212); plt.imshow(mask3)
# plt.subplot(211); plt.imshow(slice2d_u8)


plt.show()


"""
Zróbmy wydruki
1. Slice 18
2. Progowanie zwykłe
3. Progowanie pojedyncze Otsu
4. Progowanie adaptacyjne
5. Multithresh (Matlab)
"""

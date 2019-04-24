import numpy as np
import matplotlib.pyplot as plt
import pickle
from lib import VolumeData, getListOfFiles
from skimage import filters


# Wymagamy, żeby dane były w formacie uint8
path = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/fantomNowy.pckl'
vol = VolumeData(path)

slice75 = vol.getSlice(sliceNum=75)
slice75 = np.array(255 * slice75, dtype='uint8')

# fig,ax = filters.try_all_threshold(slice75)

# Yen -super!
# th_yen = filters.threshold_yen(slice75)

# Otsu - iteracyjnie
"""A jakby Otsu zrobić tak, żeby nie uwzgledniać punktów '0' ?
I w kolejnych iteracjach wymnażać przez poprzednią maskę 
"""
def thresh_otsu(image, start_point=0):
    
    nbins = 256 - start_point
    hist = np.histogram(image, range=[start_point,255], bins=nbins)[0]
    bin_centers = np.arange(nbins)
    hist = hist.astype(float)

    # class probabilities for all possible thresholds
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # class means for all possible thresholds
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]

    # Clip ends to align class 1 and class 2 variables:
    # The last value of `weight1`/`mean1` should pair with zero values in
    # `weight2`/`mean2`, which do not exist.
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    idx = np.argmax(variance12)
    threshold = bin_centers[:-1][idx] + start_point
    
    return threshold

# th_otsu_1 = filters.threshold_otsu(slice75)
# Otsu będzie zwracał punkt startowy dla kolejnych iteracji
th1 = thresh_otsu(slice75)
th2 = thresh_otsu(slice75, th1)
th3 = thresh_otsu(slice75, th2)

segData = np.zeros([*slice75.shape, 3], dtype='uint8')
for i in slice75.shape[0]:
    for j in slice75.shape[1]:
        if slice75[i,j]



import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib
from lib import VolumeData, vol2Img3D, arr2img

"""
1. Wczytanie obrazu fantoma z pliku i pobranie slice'u (przekroju)
2. Progowanie:
   - wyciąganie progów z (wygładzonego) histogramu
   - progowanie adaptacyjne
   - progowanie iteracyjne
4. Wykrywanie krawędzi
"""

# 1. Wczytanie i wyświetlenie przekrojów fantoma

FantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'
dataFilePath = FantomPath + '/data.pckl'

fantomVolume = VolumeData(dataFilePath)
# fantomVolume.showAllSlicesInOne()     # Prezentacja wszystkich przekrojów obok siebie
sliceNum = 16
slice2d = fantomVolume.getSlice(sliceNum)
# plt.imshow(slice2d)                   # Prezentacja pojedynczego przekroju
# plt.show()


# 2. Implementacja algorytmu segmentującego przez progowanie

# Histogram próbek
# bins - równoodległe punkty na osi x
bincCount = 200
bins = np.arange(0, 1, 1/bincCount)
hist, edges = np.histogram(slice2d, bins=bins)
plt.plot(hist)
plt.yscale('log')
plt.show()


# Jak dobrać parametr bins ?
# Histogram dzieli zakres maksymalnych 
"""
arr = np.random.rand(100,100)
bins = np.arange(0,1,0.001)
hista, bin_edges = np.histogram(arr, bins=10)
plt.plot(hista,'ro')
plt.show()
"""
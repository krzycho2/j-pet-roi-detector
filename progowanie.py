import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib
from lib import VolumeData, vol2Img3D, arr2img

"""
1. Wczytanie obrazu fantoma z pliku
2. Pobranie slice'u (przekroju)
3. Progowanie:
   - wyciąganie progów z (wygładzonego) histogramu
   - progowanie adaptacyjne
   - progowanie iteracyjne
4. Wykrywanie krawędzi
"""

FantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'
dataFilePath = FantomPath + '/data.pckl'
fantomVolume = VolumeData(dataFilePath)
slice18 = fantomVolume.getSlice(18)
plt.imshow(slice18)
plt.show()



# ------Stara implementacja -----------------------------

# Histogram próbek
# bins - równoodległe punkty na osi x
# bins = np.arange(0,1,0.0001)
# hist = np.histogram(dataz0[:,0], dataz0[:,1], bins=bins)
# plt.plot(bins,hist)
# plt.show()


# Jak dobrać parametr bins ?
# Histogram dzieli zakres maksymalnych 
"""
arr = np.random.rand(100,100)
bins = np.arange(0,1,0.001)
hista, bin_edges = np.histogram(arr, bins=10)
plt.plot(hista,'ro')
plt.show()
"""
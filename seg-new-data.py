# Tu będziemy wczytywać a następnie segmentować nowe pliki z rekonstrukcji

import numpy as np
import matplotlib.pyplot as plt
import pickle
from lib import VolumeData, getListOfFiles

# Wczytywanie obrazów - podać ścieżkę do folderu z rozpakowanymi plikami txt. Mogą to być też pliki pickle
fantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'
files = getListOfFiles(fantomPath + '/Nowe-reko')
volList = []
leng = len(files)

# Wczytanie danych do listy obiektów VolumeData
for i in range(leng):
    print(f'Rekonstrukcja nr {i} z {leng}')
    vol = VolumeData(files[i])
    volList.append(vol)

# Zaprezentowanie wszystkich przekrojów każdej rekonstrukcji - odkomentować
"""
for volume in volList:
    volume.showAllSlicesInOne()
"""
# Ewentualnie pokazanie poszczególnych slice'ów - odkomentować 
"""
vol0 = volList[0]
sliceNum = 10
slice1 = vol0.getSlice(sliceNum=sliceNum)
plt.imshow(slice1)
plt.title(vol0._fileName)
plt.show()
"""
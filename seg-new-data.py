# Tu będziemy wczytywać a następnie segmentować nowe pliki z rekonstrukcji

import numpy as np
import matplotlib.pyplot as plt
import pickle
from lib import VolumeData,getListOfFiles

# Wczytywanie obrazów
fantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'
files = getListOfFiles(fantomPath + '/Nowe-reko')
volList = []
leng = len(files)
for i in range(leng):
    print(f'Rekonstrukcja nr {i} z {leng}')
    vol = VolumeData(files[i])
    volList.append(vol)

for volume in volList:
    volume.showAllSlicesInOne()
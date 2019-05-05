"""Implementacje algorytmów segmentacji: 
- progowanie Yen'a
- progowanie Otsu wielowartościowe + Region Growing
- progowanie Otsu iteracyjne
"""
from skimage.filters import threshold_yen
from volumeData import VolumeData, segmentDataByThresholds
from matplotlib import pyplot as plt
import numpy as np

def yen(volume):
    """
    Argumenty
        volume: numpy.ndarray lub VolumeData 

    Wartość zwracana
        Posegmentowana macierz 3D: numpy.ndarray
    """

    if isinstance(volume, VolumeData):
        volume = volume.data3D

    thresh = threshold_yen(volume)
    segVolume = segmentDataByThresholds(volume, thresh)

    return segVolume



# Testy
path = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/fantomNowy.pckl'
vol = VolumeData(path)
segVol = VolumeData(yen(vol.data3D))
segVol.showAllSlicesInOne('Segmentacja metodą Yena')

import numpy as np
import pickle

dataFilePath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom/data.pckl'
with open(dataFilePath) as f:
    data3D = pickle.load(f)

# Histogram próbek

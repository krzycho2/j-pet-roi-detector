import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pickle
data = []
fantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'

# Odczytanie danych z pliku tekstowego
rawPath = fantomPath + '/fantom2.txt'
with open(rawPath) as f:
    lines = f.readlines()

for s in lines:
    a = s.split()
    data.append(a)
data3D = np.array(data, dtype="float32")  # Konwersja do numpy.array

# Zapis zmiennej do pliku
dataFilePath = fantomPath + '/data.pckl'
with open(dataFilePath, 'wb') as f:
	pickle.dump(data3D, f)

dataz0 = []

# z_unique - Niepowtarzające się z -> Slice'y na różnych wysokościach
z_unique = np.array(list(set(data3D[:,2])))

# Sprawdzenie liczby slice'ów:
# liczba_sliecow = len(z_unique)

# Wybór slice'u
z0 = z_unique[18]

for i in range(len(data3D)):
    if data3D[i,2] == z0:
        c = np.concatenate((data3D[i,:2], data3D[i,3:])) 
        dataz0.append(c)

dataz0 = np.array(dataz0)

# Wyświetlenie jednej z płaszczyzn
plt.scatter(x=dataz0[:,0], y=dataz0[:,1], c=dataz0[:,2], cmap='hot')
plt.show()
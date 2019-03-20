import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy import interpolate
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

# Zapis zmiennej do pliku
dataz0FilePath = fantomPath + '/dataz0.pckl'
with open(dataz0FilePath, 'wb') as f:
	pickle.dump(dataz0, f)

# Jak z tablicy 14641x3 zrobić tablicę 121x121, gdzie dla odpowiednich (x,y) była wartość z tomografu
# Czyli przerobienie macierzy punktów do obrazu (x,y)
arrSize = np.sqrt(len(data3D))
img = np.zeros([121,121])
licz = 0
for i in range(121):
    for j in range(121):
        img[120-j,i] = dataz0[licz,2]
        licz += 1

# plt.imshow(img)
# plt.show()

# Histogram
binsCount = 200     # Na tym najlepiej widać
hist, edges = np.histogram(img, bins=binsCount, range=(0,1), density=True)

# Wygładzanie histogramu
# ...
plt.plot(edges[1:binsCount], hist[1:])
plt.yscale('log')
plt.show()

# Progowanie ręczne - trzeba będzie zrobić to metodą Otsu
# Będą trzy progi 
p1 = 0.08
p2 = 0.38
p3 = 0.47
p4 = 0.59

img2 = np.zeros([121,121,3])


for i in range(121):
    for j in range(121):
        if img[i,j] < p1:
            img2[i, j, :] = [0.0, 0.0, 0.0]
        elif img[i,j] >= p1 and img[i,j] < p2:
            img2[i, j, :] = [0.0, 0.0, 255.0]
        elif img[i,j] >= p2 and img[i,j] < p3:
            img2[i, j, :] = [0.0, 255.0, 0.0]
        elif img[i,j] >= p3 and img[i,j] < p4:
            img2[i, j, :] = [0.0, 255.0, 0.0]
        else:
            img2[i, j, :] = [255.0, 255.0, 255.0]

plt.imshow(img2)
plt.title('Wynik segmentacji po ręcznym wyborze progów')
plt.show()
plt.imsave('original.png', img)

# Wyświetlenie jednej z płaszczyzn
# plt.scatter(x=dataz0[:,0], y=dataz0[:,1], c=dataz0[:,2], cmap='hot')
# plt.show()
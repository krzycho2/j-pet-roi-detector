import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib

FantomPath = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/Fantom'
dataFilePath = FantomPath + '/data.pckl'
dataz0Path = FantomPath + '/dataz0.pckl'
with open(dataFilePath, 'rb') as f:
    data3D = pickle.load(f)

with open(dataz0Path, 'rb') as f:
    dataz0 = pickle.load(f)

# Jak z tablicy 14641x3 zrobić tablicę 121x121, gdzie dla odpowiednich (x,y) była wartość z tomografu
img = np.zeros([121,121])
licz = 0
for i in range(121):
    for j in range(121):
        img[120-j,i] = dataz0[licz,2]
        licz += 1

plt.imshow(img)
plt.show()
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
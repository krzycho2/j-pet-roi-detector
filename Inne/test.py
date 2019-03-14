import numpy as np
import matplotlib.pyplot as plt
import matplotlib
data = []

# Odczytanie danych z pliku tekstowego
with open("fantom2.txt") as f:
    lines = f.readlines()

for s in lines:
    a = s.split()
    data.append(a)
data = np.array(data, dtype="float32")  # Konwersja do numpy.array

dataz0 = []

# z_unique - Niepowtarzające się z -> Slice'y na różnych wysokościach
z_unique = np.array(list(set(data[:,2])))

# Sprawdzenie liczby slice'ów:
# liczba_sliecow = len(z_unique)


for i in range(len(data)):
    if data[i,2] == z_unique[16]:
        c = np.concatenate((data[i,:2], data[i,3:])) 
        dataz0.append(c)

dataz0 = np.array(dataz0)

# img = np.zeros((len(data), len(data)))
# plt.imshow(data2d)
# plt.plot()
# plt.plot(data[:, 0], data[:,3])
# plt.show()

# Wyświetlenie jednej z płaszczyzn
plt.scatter(x=dataz0[:,0], y=dataz0[:,1], c=dataz0[:,2], cmap='hot')
plt.show()

# Pokażmy przekrój dla z = 0

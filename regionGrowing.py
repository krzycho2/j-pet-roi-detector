import numpy as np
import matplotlib.pyplot as plt
from volumeData import VolumeData
from skimage.filters import threshold_yen
from skimage.measure import label, regionprops
from skimage.morphology import closing, square

def srednia(arr, thresh):

    # print('Tab: ', arr)
    liczbaElementow = np.count_nonzero(arr >= thresh)
    if liczbaElementow == 0:    # Nie dzielimy przez 0
        return None

    idxs = np.nonzero(arr >= thresh)
    suma = sum(arr[idxs])
    # print(f'Suma: {suma}, Liczba elementów: {liczbaElementow}')
    return suma / liczbaElementow

def sigma(arr, thresh):
    """Odchylenie standardowe liczb powyżej progu"""
    temp = arr - srednia(arr, thresh)
    var = srednia((arr - srednia(arr,thresh))**2, thresh)
    if var is None:     # Tylko wtedy gdy mamy w macierzy jeden element
        return 0
    else:
        return np.sqrt(var)

def pointsInRadius(sPoint, radius, dims=2):
    points = []
    if radius == 0:
        points = [sPoint]
    else:
        # Dodanie pionowych
        for row in [sPoint[0] - radius, sPoint[0] + radius]:
            [points.append([row, col]) for col in range(sPoint[1] - radius, sPoint[1] + radius + 1)]
        
        # Dodanie poziomych
        for col in [sPoint[1] - radius, sPoint[1] + radius]:
            [points.append([row, col]) for row in range(sPoint[0] - radius + 1, sPoint[0] + radius)]

    return points

def belongsToArr(p, arr):
    """
    Sprawdza czy punkt lub zbiór punktów należy(należą) do macierzy.
    Jeśli p: punkt (2D lub 3D) to:
        True, jeśli punkt należy do macierzy
        False wpp
    Jeśli p: zbiór punktów (2D lub 3D) to:
        True, jeśli PRZYNAJMNIEJ JEDEN punkt należy do macierzy
        False, jeśli ŻADEN punkt nie należy do macierzy 
    """
    p = np.array(p)
    if len(p.shape) == 1:
        # punkt
        if len(p) == 2:     # 2D
            # Dorobić wyjątki gdy wymiary się nie zgadzają
            logic = p[0] >= 0 and p[0] < arr.shape[0] and p[1] >= 0 and p[1] < arr.shape[1]
            if logic:
                return True
            else:
                return False
        
        else:       # 3D
            logic = p[0] >= 0 and p[0] < arr.shape[0] and p[1] >= 0 and p[1] < arr.shape[1] and p[2] >= 0 and p[2] < arr.shape[2]
            if logic:
                return True
            else:
                return False
        
    else:
        # zbiór punktów. Sprawdzamy, czy choć jeden punkt/woksel jest na macierzy
        if len(p[0]) == 2:  # 2D
            for point in p:
                logic = point[0] >= 0 and point[0] < arr.shape[0] and point[1] >= 0 and point[1] < arr.shape[1]
                if logic:
                    return True
            return False
        
        else:       # 3D
            for point in p:
                logic = point[0] >= 0 and point[0] < arr.shape[0] and point[1] >= 0 and point[1] < arr.shape[1] and point[2] >= 0 and point[2] < arr.shape[2]
                if logic:
                    return True
           
            return False


# Dane wejściowe
# arr =np.random.randint(100, size=(100,100))
# thresh = 50
# startPoint = (0,0)
# arr[startPoint] = 51
c = 1

# Już na serio
path = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/fantomNowy.pckl'
vol = VolumeData(path)

arr = vol.getSlice(75)
thresh = threshold_yen(arr)
bw = closing(arr > thresh, square(3))
label_image = label(bw)

centroidy = []
for region in regionprops(label_image):
    # take regions with large enough areas
    if region.area >= 10:
        centroidy.append(region.centroid)

centroidy = np.array(centroidy)
startPoints = np.around(centroidy).astype(int)
startPoint= startPoints[2]

# def regionGrowing(arr, thresh, c = 1, startPoint=None):
if startPoint is None:
    if len(arr.shape) == 2:
        startPoint = [0,0]
    elif len(arr.shape) == 3:
        startPoint = [0,0,0]


region = [startPoint]
regionArr = np.array(region)
tempArr = arr[regionArr[:,0], regionArr[:,1]]
avg = srednia(tempArr, thresh)      # Początkowo
sigma0 = 30
sigmaC = sigma0
licznikTrafien = 0
R = 1


# Pętla po pikselach/wokselach wychodząc z punktu startPoint promieniście rozchodzi się algorytm
while(True):
    print(f'Promień: {R}')
    points = pointsInRadius(startPoint, R, 2)
    if not belongsToArr(points, arr):    # Sprawdzenie, czy przynajmniej jeden punkt należy do macierzy
        print('Wyjście poza macierz wszystkich punktów.')
        break

    licznikTrafien = 0
    for p in points:
        # p - współrzędne punktu 
        if belongsToArr(p, arr):
            print(f'Punkt {p}: {arr[p[0], p[1]]}')
            tempWynik = abs(arr[p[0], p[1]] - avg)
            print(f'tempWynik: {tempWynik}, sigmaC: {sigmaC}')
            if tempWynik <= sigmaC:
                region.append(p)
                print('Dodany')
                licznikTrafien += 1
                regionArr = np.array(region)
                tempArr = arr[regionArr[:,0], regionArr[:,1]]
                avg = srednia(tempArr, thresh)      # Początkowo
                sigmaC = c * sigma(tempArr, thresh)
                if sigmaC == 0:
                    sigmaC = sigma0
                print('srednia:', avg)
                print('sigma:', sigmaC)
    
    # Jeśli licznik jest 0 to zakończ pętlę
    if licznikTrafien == 0 :
        print('Brak trafień dla promienia R=', R)
        break

    R += 1

newArr = np.zeros(arr.shape)
r = np.array(region)
newArr[r[:,0], r[:,1]] = 255

plt.subplot(1,2,1); plt.imshow(arr)
plt.subplot(1,2,2); plt.imshow(newArr)
plt.show()
# print(f'Wartości regionu: {arr[r[:,0], r[:,1]]}')


# p = np.array(pointsInRadius((0,0), 2))
# print(p)

# punkt = [[0,0], [3,3]]
# macierz = np.arange(4).reshape(2,2)
# print(belongsToArr(punkt, macierz))
# thresh = 5
# arr = np.random.randint(1,10, (1,10))
# print('srednia: ', srednia(arr,thresh))
# print('sigma: ', sigma(arr, thresh))

# Wyprodukować macierz
# I wypróbować regionGrowing
  
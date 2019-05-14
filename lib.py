import numpy as np
# import pickle
import os
# import matplotlib.pyplot as plt
# import random
# import itertools
# Różne przydatne metody

def multiThreshOtsu(image):
    """
    Narazie dla 2D i nie do końca działa. Będzie wkrótce...
    """
    N = np.count_nonzero(image != 0)
    hist = np.histogram(image, bins=maxVal)[0]
    hist[0] = 0         # Nie uwzględnianie zera

    w0k, w1k, w2k   = 0,0,0       # Jakieś wagi, double
    m0k, m1k, n2k   = 0,0,0       # Średnie 
    m0, m1, m2      = 0,0,0
    m0k, m1k, mt    = 0,0,0
    currVar         = 0
    thresh1, thresh2= 0,0
    maxBetweenVar   = 0

    # Oryginał
    # for k in range(maxVal):
    #         mt += k * hist[k] / N

    # for k in range(maxVal):
    #     mt += k * hist[k] / N

    mt2 = np.sum(np.arange(maxVal) * hist / N)

    for t1 in range(maxVal):
        w0k += hist[t1] / N
        m0k += t1 * hist[t1] / N
        m0 = m0k / w0k
        # print(f't1: {t1}, hist[t1]: {hist[t1]}, w0k: {w0k}, m0k: {m0k}, m0: {m0}')

        w1k, m1k = 0,0
        for t2 in range(t1+1, maxVal):
            w1k += hist[t2] / N
            m1k += t2 * hist[t2] / N
            m1 = m1k / w1k
            # print(f'    t2: {t2}, hist[t2]: {hist[t2]}, w1k: {w1k}, m1k: {m1k}, m1: {m1}')

            w2k = 1 - (w0k + w1k)
            m2k = mt - (m0k + m1k)
            
            if w2k <= 0:
                # print('w2k < 0')
                break
            m2 = m2k / w2k
            # print(f'    w2k: {w2k}, m2k: {m2k}, m2: {m2}')

            currVar = w0k * (m0 - mt)**2 + w1k * (m1 - mt)**2 + w2k * (m2 - mt)**2
            # print(f'    currVar: {currVar}')

            if maxBetweenVar < currVar:
                maxBetweenVar = currVar
                thresh1 = t1
                thresh2 = t2

    return [thresh1, thresh2]

    
def threshOtsu(image, start_point=0):
    
    nbins = 256 - start_point
    hist = np.histogram(image, range=[start_point,255], bins=nbins)[0]
    bin_centers = np.arange(nbins)
    hist = hist.astype(float)

    # class probabilities for all possible thresholds
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # class means for all possible thresholds
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]

    # Clip ends to align class 1 and class 2 variables:
    # The last value of `weight1`/`mean1` should pair with zero values in
    # `weight2`/`mean2`, which do not exist.
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    idx = np.argmax(variance12)
    threshold = bin_centers[:-1][idx] + start_point
    
    return threshold

def pointsInRadius(sPoint, radius):
    """
    Tworzy zbiór (listę) punktów odległych od punktu środkowego sPoint o promień radius. 
    Fizycznie będzie to zbiór punktów płaszczyzny kwadratu o boku 2*radius + 1, w którego centroidzie znajduje się sPoint. 
    """
    points = []
    if radius == 0:
        points = [sPoint]
    else:
        
        # Przypadek 2D
        if len(sPoint) == 2:
            # Dodanie pionowych
            for row in [sPoint[0] - radius, sPoint[0] + radius]:
                [points.append([row, col]) for col in range(sPoint[1] - radius, sPoint[1] + radius + 1)]
            
            # Dodanie poziomych
            for col in [sPoint[1] - radius, sPoint[1] + radius]:
                [points.append([row, col]) for row in range(sPoint[0] - radius + 1, sPoint[0] + radius)]
            
        # Przypadek 3D
        else:
            z = sPoint[2]
            for row in [sPoint[0] - radius, sPoint[0] + radius]:
                [points.append([row, col, z]) for col in range(sPoint[1] - radius, sPoint[1] + radius + 1)]

            for col in [sPoint[1] - radius, sPoint[1] + radius]:
                [points.append([row, col, z]) for row in range(sPoint[0] - radius + 1, sPoint[0] + radius)]

            for z in [sPoint[2] - radius, sPoint[2] + radius]:
                for row in range(sPoint[0] - radius, sPoint[0] + radius + 1):
                    for col in range(sPoint[1] - radius, sPoint[1] + radius + 1):
                        points.append([row, col, z])

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

def points2Img3D(rawData):
    """
    Konwertuje wolumem 3D z postaci N x {x,y,z,f(x,y,z)} do postaci sqrt(Nx) x sqrt(Ny) x Nz
    """

    ind = np.lexsort((rawData[:,2], rawData[:,1], rawData[:,0]))    # Sortowanie danych
    rawData = rawData[ind]
    
    Nx = len(set(rawData[:,0]))
    Ny = len(set(rawData[:,1]))
    Nz = len(set(rawData[:,2]))
    
    licz = 0
    img3D = np.zeros((Nx,Ny,Nz))
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                img3D[Ny-1-j,i,k] = rawData[licz,3]          # Przekopiowanie danych
                licz += 1
    
    return img3D

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

def arr2img(arr):
    """
    Konwertuje macierz N x 3  która w kolejnych wierszach ma współrzędne oraz wartości punktów
    arr: len(a[0]) = 3 - a[0:2] - x,y, a[2] - f(x,y) 
    len(arr) musi być kwadratem liczby całkowitej
    """
    N = int(np.sqrt(len(arr)))
    img = np.zeros((N,N))

    licz = 0
    for i in range(N):
        for j in range(N):
            img[N-1-j,i] = arr[licz,2]
            licz += 1
    return img


#########
# STAŁE #
#########

KROTKIE_INFO = """
            Program SegmentujObrazyJPET
            by Krzysztof Krupiński 2019
Poprawne wywołanie segmentacji:

python SegmentujObrazyJPET.py [yen | otsu-region | otsu-iter] [ścieżka_do_pliku_z_rekonstrukcją]

Żeby uruchomić pełną wersję programu wraz z uzyskaniem informacji na temat algorytmów segmentacji wprowadź

python SegmentujObrazyJPET.py
"""

TEKST_POWITALNY = """ 
            Witamy w programie SegmentujObrazyJPET
                by Krzysztof Krupiński 2019
 
OPIS PROGRAMU
Program jest narzędziem służącym do segmentacji obrazów 3D (wolumenów)
pochodzących z rekonstrukcji obrazowania tomografem pozytonowym.

Segmentacja może być wkonana za pomocą następujących algorytmów:
- algorytm progujący Yena
- algorytm progujący Otsu w połączeniu z algorytmem Region Growing
- iteracyjny algorytm Otsu.
Szczegółowe informacje można uzyskać wpisując poniżej polecenie:

info [yen | otsu-region | otsu-iter]

INSTRUKCJA UŻYCIA
Aby wykonać segmentację wpisz polecenie

run [yen | otsu-region | otsu-iter] [ścieżka_do_pliku_z_rekonstrukcją]

Plik z rekonstrukcją może być typu tekstowego (.txt) lub jako macierz
zapisana do pliku .pckl. Dane w pliku muszą być ułożone w następujących
konfiguracjach:
- macierz Nx4, gdzie kolumny to x,y,z,f(x,y,z)
- macierz trójwymiarowa KxLxM, gdzie dla każdego punktu w przestrzeni
  (x,y,z) przydzielona jest wartość emisyjności.

Aby zakończyć pracę z programem wpisz polecenie 
exit
lub ctrl+c.

    """

INFO = """
Możliwe polecenia:

info [yen | otsu-region | otsu-iter]
run [yen | otsu-region | otsu-iter] [ścieżka_do_pliku_z_rekonstrukcją]
exit
"""

INFO_INFO = """ Informacje o algorytmie można uzyskać wpisując

info [yen | otsu-region | otsu-iter]
"""
INFO_RUN = """ Segmentację wykonuje się wpisując

run [yen | otsu-region | otsu-iter] [ścieżka_do_pliku_z_rekonstrukcją]

gdzie ścieżka musi mieć rozszerzenie .txt lub .pckl
"""

INFO_YEN = """
Algorytm segmentacji Yen
"""

INFO_YEN_REGION = """
Algorytm Region Growing w połączeniu z progowaniem Yen'a
"""

INFO_OTSU_ITER = """
Algorytm Otsu iteracyjny"""

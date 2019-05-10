import numpy as np
# import pickle
import os
# import matplotlib.pyplot as plt
# import random
# import itertools
# Różne przydatne metody

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

def otsuMultiThresh(image):
    maxVal = 256
    
    # Histogram
    # hist = np.histogram(image, bins=maxVal)[0]
        
    N = 0 # Licznik niezerowych punktów
    hist = np.zeros(maxVal)
    for i in range(h):
        for j in range(w):
            val = slice75[i,j]
            if val != 0:
                hist[val] += 1
                N += 1

    # N = 1
    # for s in image.shape:   # 2d lub 3d
    #     N *= s
    
    w0k, w1k, w2k   = 0,0,0       # Jakieś wagi, double
    m0k, m1k, n2k   = 0,0,0       # Średnie 
    m0, m1, m2      = 0,0,0
    m0k, m1k, mt    = 0,0,0
    currVar         = 0
    thresh1, thresh2= 0,0
    maxBetweenVar   = 0

    for k in range(maxVal):
        mt += k * hist[k] / N

    # plt.plot(np.arange(256), hist)
    # plt.show()


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

        return (thresh1, thresh2)

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

krotkieInfo = """
            Program SegmentujObrazyJPET
            by Krzysztof Krupiński 2019
Poprawne wywołanie segmentacji:

python SegmentujObrazyJPET.py [yen | otsu-region | otsu-iter] [ścieżka_do_pliku_z_rekonstrukcją]

Żeby uruchomić pełną wersję programu wraz z uzyskaniem informacji na temat algorytmów segmentacji wprowadź

python SegmentujObrazyJPET.py
"""

tekstPowitalny = """ 
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

info = """
Możliwe polecenia:

info [yen | otsu-region | otsu-iter]
run [yen | otsu-region | otsu-iter] [ścieżka_do_pliku_z_rekonstrukcją]
exit
"""

infoInfo = """ Informacje o algorytmie można uzyskać wpisując

info [yen | otsu-region | otsu-iter]
"""
infoRun = """ Segmentację wykonuje się wpisując

run [yen | otsu-region | otsu-iter] [ścieżka_do_pliku_z_rekonstrukcją]

gdzie ścieżka musi mieć rozszerzenie .txt lub .pckl
"""

infoYen = """
Algorytm segmentacji Yen
"""

infoOtsuRegion = """
Algorytm Otsu Region Growing
"""

infoOtsuIter = """
Algorytm Otsu iteracyjny"""

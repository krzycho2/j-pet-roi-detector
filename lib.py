import numpy as np
# import pickle
import os
# import matplotlib.pyplot as plt
# import random
# import itertools
# Różne przydatne metody

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

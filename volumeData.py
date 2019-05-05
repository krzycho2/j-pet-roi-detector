import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import random
import itertools

class VolumeData():
    """
    Obiekty tej klasy wykonują operacje na plikach z rekonstrukcji (odczyt, zapis do pliku).
    Dozwolone formaty plików: 
    - tekstowy .txt
    - pickle .pckl - wygodny format zapisu ZMIENNYCH do pliku w Pythonie
    
    Dane mogą być podane jako:
    - macierz N x 4 - kolumny to {x, y, z, intensywność}, a wiersze to kolejne pomiary
    - obrazy {x,y,z} (macierze 3D)  
    
    Obrazy można zapisać do plików pickle jako macierze 3D
    Obiekty posiadają atrybuty:
    - data3D - macierz punktów 3D
    - fileName - końcowa nazwa pliku

    Obiekty posiadają metody:
    - init(filePath) - konstruktor. Jako argument podawana jest ścieżka do pliku.
    - savePickle(filePath) - zapis danych (macierz 3D) do pliku pickle pod zadaną nazwą
    - getSlice(sliceNUM) - zwraca macierz 2D (obraz) konkretnego przekroju
    - showAllSlicesInOne() - wyświetla wszystkie przekroje obok siebie na jednym figure 
    """

    
    @property
    def data3D(self):
        return self._data3D

    @property
    def fileName(self):
        return self, _fileName
    
    def __init__(self, inputData, dataType='float'): 
        """
        Tworzy obiekt data3D przechowujący obraz 3D z tomografu.

        Argumenty

            inputData (string lub array): Dane wejściowe. Mogą pochodzić z:
            - pliku txt lub pickle
            - macierzy Nx4 (x, y, z, f{x,y,z}) lub PxQxR

            dataType (string): do wyboru:
            - 'float' - dane formatowane do flaot 32 bitowego, wartości z przedziału [0,1] 
            - 'uint8' - format 8 bitowy, dane z przedziału [0,255]
        
        """
        # Do zaimplementowania - różne typy danych. W sumie lepiej jak będzie uint8 - znana z góry liczba możliwych wartości
        # Trzeba też uwzględnić możliwość tworzenia obiektów na podstawie macierzy
        ext = os.path.splitext(inputData)[1]     # Pobranie nazwy pliku i rozszerzenia

        # Kontrola poprawności danych 
        # Jeśli zły typ danych wejściowych to zwrócenie None
        if not (isinstance(inputData, np.ndarray) or isinstance(inputData, str)):
            print(f'Zły typ danych wejściowych inputData. Oczekiwane: numpy.array lub str. Podano {type(a)}.')
            return None

        # Jeśli ścieżka nie ma rozszerzenia txt lub None
        if ext is not '.txt' and ext is not '.pickle':
            print('Niepoprawna ścieżka do pliku z danych. Dozwolone są ścieżki z rozszerzeniami .txt lub .pckl')
            return None

        # Jeśli podano zły typ danych WYJŚCIOWYCH to zwrócenie None
        if  dataType is not 'float' and dataType is not 'uint8':
            print(f'Niepoprawny typ danych. Oczekiwano float lub uint8. Podano {dataType}.')
            return None


        self._fileName = os.path.basename(os.path.normpath(inputData))
        rawData = []   # Pusta macierz

        if ext == '.txt':        # Dane podane w formacie tekstowym
            print('Wykryto plik .txt')
            with open(filePath) as f:
                lines = f.readlines()
            data = []
            for s in lines:
                a = s.split()
                data.append(a)
            rawData = data

        # Drugi przypadek - dane podane w formacie pickle
        elif ext == '.pckl':
            print('Wykryto plik .pickle')
            with open(filePath, 'rb') as f:
                rawData = pickle.load(f)


        dane = np.array(dane, dtype="float32")
        if len(dane[0]) == 4 and len(dane.shape) == 2:   # Sprawdzenie czy 2 wymiary i 4 kolumny
            self._data3D = points2Img3D(dane)  # Konwersja do wolumenu 3D 
            print('2 wymiary, 4 kolumny - konwersja do wolumenu 3D')
            print(f'Dane mają wymiary: {self._data3D.shape}')
        elif len(dane.shape) == 3:   # Sprawdzenie czy 3 wymiary   
            self._data3D = dane              # Nic nie zmieniać 
            print('3 wymiary - nie zmieniać')
            print(f'Dane mają wymiary: {self._data3D.shape}')
        else:
            self = None
            print('Niepoprawny typ danych')
        

    def savePickle(self, filePath = __name__ + 'Data.pckl'):    
        "Zapisuje dane jako plik pickle"
        with open(filePath, 'wb') as f:
	        pickle.dump(self.data3D, f)

    def getSlice(self, sliceNum=None, deep=None):     
        "sliceNum - numer przekroju, deep - 'głębokość w objętości podana jako liczba z przedziału (0,1)"
        if sliceNum != None and deep == None:
            return self._data3D[:,:,sliceNum]
        elif deep != None and sliceNum == None:
            sliceNum = int(deep * self._data3D.shape[2])
            return self._data3D[:,:,sliceNum]
        else:
            print('getSlice: Niepoprawna liczba argumentów')

    def showAllSlicesInOne(self):
        "Tworzy kolarz ze wszystkich przekrojów wolumenu"
        # Niech będzie 6 rzędów
        Nz = self._data3D.shape[2]   # Liczba przekrojów
        maxValue = np.amax(self._data3D)
        minValue = np.amin(self._data3D)
        rows = 6
        cols = Nz//rows + 1
        fig = plt.figure(self._fileName)
        for index in range(0,Nz):
            ax = fig.add_subplot(rows,cols,index+1)
            ax.imshow(self.getSlice(sliceNum=index), vmin=minValue, vmax=maxValue)
            ax.set_title( index )
        
        plt.show()


def segmentData(image, ths):
    """Segmentuje obraz 2d lub 3d w odniesieniu do progów podanych jako argumenty"""

    ths = sorted(ths)   # Na wszelki wypadek sortowanko
    if len(ths) > 8:
        print('Nie obsługujemy tylu możliwych progów. Pozdrawiamy, ekipa lib.py')
        return None

    # Kolory
    kolory = []
    [kolory.append(x) for x in itertools.product([0,255], repeat=3)]
    # print('Kolory:', kolory)
    segData = np.zeros([*image.shape,3], dtype='uint8')
    
#    Kolorowanie element po elemencie - najmniej efektywna metoda na świecie
    if len(image.shape) == 3:
        print('Dane 3 wymiarowe')
    else:
        print('Dane 2-wymiarowe')
        
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            
            # Wolumen 3D
            if len(image.shape) == 3:     
                for k in range(image.shape[2]):
                    if image[i,j,k] < ths[0]:
                        segData[i,j,k] = kolory[0]
                    for t in range(len(ths) - 1):
                        if image[i,j,k] >= ths[t] and image[i,j,k] < ths[t+1]:
                            segData[i,j,k] = kolory[t+1]
           
            # Obraz 2D
            else:
                if image[i,j] < ths[0]:
                    segData[i,j] = kolory[0]
                for t in range(len(ths) - 1):
                    if image[i,j] >= ths[t] and image[i,j] < ths[t+1]:
                        segData[i,j] = kolory[t+1]
                if image[i,j] > ths[-1]:
                    segData[i,j] = kolory[-1]

    return segData

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
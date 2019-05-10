import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import random
import itertools
from timeit import default_timer as timer
from skimage.filters import threshold_yen
from lib import threshOtsu, points2Img3D

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
    def dataName(self):
        return self._dataName
    
    def __init__(self, inputData, dataType='uint8'): 
        """
        Tworzy obiekt data3D przechowujący obraz 3D z tomografu.

        Argumenty

            inputData (string lub array): Dane wejściowe. Mogą pochodzić z:
            - pliku txt lub pickle
            - macierzy Nx4 (x, y, z, f{x,y,z}) lub PxQxR

            dataType (string): do wyboru:
            - 'float' - dane formatowane do flaot 32 bitowego, wartości z przedziału [0,1] - narazie brak
            - 'uint8' - format 8 bitowy, dane z przedziału [0,255]
        
        """
        # Do zaimplementowania - różne typy danych. W sumie lepiej jak będzie uint8 - znana z góry liczba możliwych wartości
        # Trzeba też uwzględnić możliwość tworzenia obiektów na podstawie macierzy
        rawdata = []

        # Użytkownik podał ścieżkę do pliku
        if isinstance(inputData, str):
            ext = os.path.splitext(inputData)[1]     # Pobranie nazwy pliku i rozszerzenia
            
            if ext == '.pckl':
                print('Wczytuję dane z pliku pckl...')
                rawData = np.load(inputData)

            elif ext == '.txt':
                print('Wczytuję dane txt...')
                rawData = np.loadtxt(inputData)


            else:
                print('Niepoprawna ścieżka do pliku z danymi. Dozwolone są ścieżki z rozszerzeniami .txt lub .pckl')
                return None
            
            self._dataName = os.path.basename(os.path.normpath(inputData))

        # Użytkownik podał macierz 
        elif isinstance(inputData, np.ndarray):
            print('Wczytuję dane z macierzy...')
            rawData = inputData
            self._dataName = "Dane"

        # Jeśli nie podano macierzy ani ścieżki
        else:
            print(f'Zły typ danych wejściowych inputData. Oczekiwane: numpy.array lub str. Podano {type(a)}.')
            return None

        # Formatowanie danych do macierzy 3D uint8
         
        ksztalt = rawData.shape
        if len(ksztalt) == 2:
            if ksztalt[0] > 0 and ksztalt[1] == 4:      # Dane w formacie Nx4
                rawData = points2Img3D(rawData)
                print('Konwersja do wolumenu 3D')
            else:
                print('Niepoprawny format danych.')
                return None

        elif len(ksztalt) == 3:
            print('Brak konwersji - dane w formacie 3D')
            
        else:
            print('Niepoprawny format danych. Wymagany Nx4 lub KxLxM')
            return None

        print(f'Dane mają wymiary: {rawData.shape}')

        # Jak zostanie czasu to zaimplementować float zamiast uint8
        if isinstance(rawData.flat[0], np.float):
            if np.min(rawData) >= 0 and np.max(rawData) <= 1:
                print('Konwersja danych do uint8')
                rawData = np.array(255*rawData, dtype='uint8')
            else:
                print('Niepoprawny typ danych. Wymagany np.float (wartości 0-1 lub np.integer 0-255)')
                return None

        elif isinstance(rawData.flat[0], np.integer) or isinstance(rawData.flat[0], np.uint8):
            if np.min(rawData) >= 0 and np.max(rawData) <= 255:
                rawData = np.array(rawData, dtype='uint8')
            else:
                print('Niepoprawny typ danych. Wymagany np.float (wartości 0-1 lub np.integer 0-255)')
                return None

        self._data3D = rawData
        

    def savePickle(self, filePath = __name__ + 'Data.pckl'):    
        "Zapisuje dane jako plik pickle"
        with open(filePath, 'wb') as f:
	        pickle.dump(self._data3D, f)


    def getSlice(self, sliceNum=None, deep=None):     
        "sliceNum - numer przekroju, deep - 'głębokość w objętości podana jako liczba z przedziału (0,1)"
        if sliceNum != None and deep == None:
            return self._data3D[:,:,sliceNum]
        elif deep != None and sliceNum == None:
            sliceNum = int(deep * self._data3D.shape[2])
            return self._data3D[:,:,sliceNum]
        else:
            print('getSlice: Niepoprawna liczba argumentów')


    def showAllSlicesInOne(self, title = None):
        "Tworzy kolarz ze wszystkich przekrojów wolumenu"
        if title == None:
            title = self._dataName
        # Niech będzie 6 rzędów
        Nz = self._data3D.shape[2]   # Liczba przekrojów
        maxValue = np.amax(self._data3D)
        minValue = np.amin(self._data3D)
        rows = 6
        cols = Nz//rows + 1
        fig = plt.figure(title)
        for index in range(0,Nz):
            ax = fig.add_subplot(rows,cols,index+1)
            ax.imshow(self.getSlice(sliceNum=index), vmin=minValue, vmax=maxValue)
            ax.set_title( index )
        
        plt.show()


    def yenSegment(self):
        """
        Wykonuje segmentację metodą Yen'a

        Wartość zwracana
            Posegmentowana macierz 3D: VolumeData
        """
        thresh = threshold_yen(self._data3D)
        segVolume = self.segmentDataByThresholds(thresh)

        return segVolume


    def otsu_iterSegment(self, iterCount=3):
        """
        Wykonuje segmentację algorytmem Otsu iteracyjnie
        Wartość zwracana
            Posegmentowana macierz 3D: VolumeData
        """
        thresh = 0
        threshList = []
        for i in range(iterCount):
            thresh = threshOtsu(self._data3D, thresh)
            threshList.append(thresh)
        
        segVolume = self.segmentDataByThresholds(threshList)
        print('Znalezione prgi: ', threshList)
        
        return segVolume


    def segmentDataByThresholds(self, ths):
        """Segmentuje obraz 2d lub 3d w odniesieniu do progów podanych jako argumenty"""

        image = self._data3D
        maxThs = 8
        if not hasattr(ths, "__len__"):
            ths = [ths]

        if len(ths) > 1:
            ths = sorted(ths)   # Na wszelki wypadek sortowanko

        if len(ths) > maxThs:
            print('Nie obsługujemy tylu możliwych progów. Pozdrawiamy, ekipa segmentData.')
            return None

        # Kolory
        # kolory = []

        # Zmiana do kolorów w skali szarości
        kolory = np.linspace(0, 255, len(ths) + 1, dtype='uint8')   # Równo rozłożone wartości od czarnego do białego
        print('Kolory:', kolory)

        segData = np.zeros(image.shape, dtype='uint8')
        
    #    Kolorowanie element po elemencie - najmniej efektywna metoda na świecie
        if len(image.shape) == 3:
            print('Dane 3 wymiarowe')
        else:
            print('Dane 2-wymiarowe')

        # Wersja 1

        # for i in range(image.shape[0]):
        #     for j in range(image.shape[1]):
                
        #         # Wolumen 3D
        #         if len(image.shape) == 3:     
        #             for k in range(image.shape[2]):
        #                 if image[i,j,k] < ths[0]:
        #                     segData[i,j,k] = kolory[0]
        #                 for t in range(len(ths) - 1):
        #                     if image[i,j,k] >= ths[t] and image[i,j,k] < ths[t+1]:
        #                         segData[i,j,k] = kolory[t+1]
        #                 if image[i,j,k] >= ths[-1]:
        #                     segData[i,j,k] = kolory[-1]
            
        #         # Obraz 2D
        #         else:
        #             if image[i,j] < ths[0]:
        #                 segData[i,j] = kolory[0]
        #             for t in range(len(ths) - 1):
        #                 if image[i,j] >= ths[t] and image[i,j] < ths[t+1]:
        #                     segData[i,j] = kolory[t+1]
        #             if image[i,j] > ths[-1]:
        #                 segData[i,j] = kolory[-1]


        # Wersja 2 - oszczędność czasowa 155x
        
        d0 = np.where(image < ths[0])    # Indeksy, dla których obraz ma wartość < ths[0]
        segData[d0] = kolory[0]

        for t in range(len(ths) - 1):
            logicTrue = np.logical_and(image >= ths[t], image < ths[t+1])
            di = np.where(logicTrue)
            segData[di] = kolory[t]

        dn = np.where(image >= ths[-1])
        segData[dn] = kolory[-1]
    
        return VolumeData(segData)


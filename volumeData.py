import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import random
import itertools
from timeit import default_timer as timer
from skimage.filters import threshold_yen
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
import lib
import datetime

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
                try:
                    rawData = np.load(inputData)
                except FileNotFoundError:
                    raise ValueError

            elif ext == '.txt':
                print('Wczytuję dane txt...')
                try:
                    rawData = np.loadtxt(inputData)
                except FileNotFoundError:
                    raise ValueError

            else:
                print('Niepoprawna ścieżka do pliku z danymi. Dozwolone są ścieżki z rozszerzeniami .txt lub .pckl')
                raise ValueError
            
            self._dataName = os.path.basename(os.path.normpath(inputData))

        # Użytkownik podał macierz 
        elif isinstance(inputData, np.ndarray):
            print('Wczytuję dane z macierzy...')
            rawData = inputData
            self._dataName = "Dane"

        # Jeśli nie podano macierzy ani ścieżki
        else:
            print(f'Zły typ danych wejściowych inputData. Oczekiwane: numpy.array lub str. Podano {type(a)}.')
            raise ValueError

        # Formatowanie danych do macierzy 3D uint8
         
        ksztalt = rawData.shape
        if len(ksztalt) == 2:
            if ksztalt[0] > 0 and ksztalt[1] == 4:      # Dane w formacie Nx4
                rawData = lib.points2Img3D(rawData)
                print('Konwersja do wolumenu 3D')
            else:
                print('Niepoprawny format danych.')
                raise ValueError

        elif len(ksztalt) == 3:
            print('Brak konwersji - dane w formacie 3D')
            
        else:
            print('Niepoprawny format danych. Wymagany Nx4 lub KxLxM')
            raise ValueError

        print(f'Dane mają wymiary: {rawData.shape}')

        # Jak zostanie czasu to zaimplementować float zamiast uint8
        if isinstance(rawData.flat[0], np.float):
            if np.min(rawData) >= 0 and np.max(rawData) <= 1:
                print('Konwersja danych do uint8')
                rawData = np.array(255*rawData, dtype='uint8')
            else:
                print('Niepoprawny typ danych. Wymagany np.float (wartości 0-1 lub np.integer 0-255)')
                raise ValueError

        elif isinstance(rawData.flat[0], np.integer) or isinstance(rawData.flat[0], np.uint8):
            if np.min(rawData) >= 0 and np.max(rawData) <= 255:
                rawData = np.array(rawData, dtype='uint8')
            else:
                print('Niepoprawny typ danych. Wymagany np.float (wartości 0-1 lub np.integer 0-255)')
                raise ValueError

        self._data3D = rawData


    def savePickle(self, filePath):    
        "Zapisuje dane jako plik pickle"
        with open(filePath, 'wb') as f:
	        pickle.dump(self._data3D, f)

    def saveSlices(self, filePath, title='Segmentacja'):
        fig = self.__makeFigureWithAllSlices(figTitle=title)
        fig.savefig(filePath)

    def getSlice(self, sliceNum=None, deep=None):     
        "sliceNum - numer przekroju, deep - 'głębokość w objętości podana jako liczba z przedziału (0,1)"
        if sliceNum != None and deep == None:
            return self._data3D[:,:,sliceNum]
        elif deep != None and sliceNum == None:
            sliceNum = int(deep * self._data3D.shape[2])
            return self._data3D[:,:,sliceNum]
        else:
            print('getSlice: Niepoprawna liczba argumentów')

    def __makeFigureWithAllSlices(self, size = (20,20), figTitle = None):
        if figTitle == None:
            figTitle = self._dataName
        Nz = self._data3D.shape[2]   # Liczba przekrojów
        maxValue = np.amax(self._data3D)
        minValue = np.amin(self._data3D)
        rows = int(np.sqrt(Nz))
        cols = Nz//rows + 1
        fig = plt.figure(figsize=size)
        fig.suptitle(figTitle, fontsize=20)

        for index in range(0,Nz):
            ax = fig.add_subplot(rows,cols,index+1)
            ax.imshow(self.getSlice(sliceNum=index), vmin=minValue, vmax=maxValue)
            ax.set_title( index )
            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            frame.axes.get_yaxis().set_visible(False)
        

        return fig

    def showAllSlices(self, title = None):
        "Tworzy kolarz ze wszystkich przekrojów wolumenu"
        if title == None:
            title = self._dataName
        # Niech będzie 6 rzędów
        fig = self.__makeFigureWithAllSlices()
        
        plt.show()
        fig.savefig()
        
        return self._dataName


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
            thresh = lib.threshOtsu(self._data3D, thresh)
            threshList.append(thresh)
        
        segVolume = self.segmentDataByThresholds(threshList)
        print('Znalezione prgi: ', threshList)
        return segVolume

    def regionGrowingSegment(self, c=2, sigma0=20):
        """
        Wykonuje segmentację algorytmem Region Growing. Za punkt startowy bierze punkt z obszaru zsegmentowantego progowaniem Otsu.
        Wartość zwracana
            Posegmentowana macierz 3D: VolumeData
        """
        img = self._data3D

        trzyDe = True
        if len(img.shape) == 2:
            trzyDe = False

        thresh = threshold_yen(img)
        bw = img >= thresh
        label_image = label(bw)

        centroidy = []
        for region in regionprops(label_image):
            centroidy.append(region.centroid)

        centroidy = np.array(centroidy)
        startPoints = np.around(centroidy).astype(int)
        regions = []
        for startPoint in startPoints:

            if startPoint is None:
                if trzyDe:
                    startPoint = [0,0,0]
                else:
                    startPoint = [0,0]

            # Parametr algorytmu
            c = 2

            region = [startPoint]

            # Transformacje, które pozwolą na multiindeksowanie macierzy/obrazu
            regionArr = np.array(region)
            if trzyDe:
                tempImg = img[regionArr[:,0], regionArr[:,1], regionArr[:,2]]
            else:
                tempImg = img[regionArr[:,0], regionArr[:,1]]

            avg = np.mean(tempImg)
            sigma0 = 20
            sigmaC = sigma0

            licznikTrafien = 0
            R = 1

            # Pętla po pikselach/wokselach. Wychodząc z punktu startPoint promieniście rozchodzi się algorytm.
            while(True):
                print(f'Promień: {R}')
                points = lib.pointsInRadius(startPoint, R)
                if not lib.belongsToArr(points, img):    # Sprawdzenie, czy przynajmniej jeden punkt należy do macierzy
                    print('Wyjście poza macierz wszystkich punktów.')
                    break

                licznikTrafien = 0
                for p in points:
                    # p - współrzędne punktu 
                    if lib.belongsToArr(p, img):
                        print(f'Punkt {p}: {img[p[0], p[1], p[2]]}')
                        if trzyDe:
                            tempWynik = abs(img[p[0], p[1], p[2]] - avg)
                        else:
                            tempWynik = abs(img[p[0], p[1]] - avg)
                        print(f'tempWynik: {tempWynik}, sigmaC: {sigmaC}')

                        if tempWynik <= sigmaC:
                            region.append(p)
                            print('Dodany')
                            licznikTrafien += 1

                            # Transformacje, które pozwolą na multiindeksowanie macierzy/obrazu
                            regionArr = np.array(region)
                            
                            if trzyDe:
                                tempImg = img[regionArr[:,0], regionArr[:,1], regionArr[:,2]]
                            else:
                                tempImg = img[regionArr[:,0], regionArr[:,1]]
        
                            avg = np.mean(tempImg)
                            sigmaC = c * np.sqrt(np.var(tempImg))

                            if sigmaC == 0:
                                sigmaC = sigma0
                
                            print('srednia:', avg)
                            print('sigma:', sigmaC)
                
                # Jeśli licznik jest 0 to zakończ pętlę
                if licznikTrafien == 0 :
                    print('Brak trafień dla promienia R=', R)
                    break

                R += 1
        r = np.array(region)
        regions.append(r)

        newImg = np.zeros(img.shape, dtype='uint8')

        for r in regions:
            if trzyDe:
                newImg[r[:,0], r[:,1], r[:,2]] = 255
            else:
                newImg[r[:,0], r[:,1]] = 255

        segImage = VolumeData(newImg)
        return segImage

    def otsuMultiThreshSegment(self):
        """
        Segmentuje obraz za pomocą wielowartościowego (2) progowania Otsu.
        """
        thresholds = lib.multiThreshOtsu(self._data3D)
        segImage = self.segmentDataByThresholds(thresholds)

        return segImage

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
    
        d0 = np.where(image < ths[0])    # Indeksy, dla których obraz ma wartość < ths[0]
        segData[d0] = kolory[0]

        for t in range(len(ths) - 1):
            logicTrue = np.logical_and(image >= ths[t], image < ths[t+1])
            di = np.where(logicTrue)
            segData[di] = kolory[t+1]

        dn = np.where(image >= ths[-1])
        segData[dn] = kolory[-1]
    
        return VolumeData(segData)


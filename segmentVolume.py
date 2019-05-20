from volumeData import VolumeData
import lib
from skimage.filters import threshold_yen
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
import numpy as np
import os
import datetime

class SegmentVolume():
    """
    Obiekty tej klasy wykonują segmentacje różnymi metodami, a potem wyniki zapisuje do pliku.
    """
    # Gettery, prezentacja pól
    # Ścieżka z plikami po segmentacji
    @property
    def segmentDir(self):
        return self.__segmentDir

    # Surowe dane
    # Typ: VolumeData
    @property
    def rawVolume(self):
        return self.__rawVolume

    # Posegmentowane dane
    # Typ: VolumeData
    @property
    def segmentedVolume(self):
        return self.__segmentedVolume

    # Słownik działających algorytmów
    @property
    def algorithms(self):
        return self.__algorithms.keys()

    @property
    def algName(self):
        return self.__algName

    # Inicjalizator
    def __init__(self, inputData):
        """
        Konstruktor
        Sprawdza, czy nazwa algorytmu oraz dane są ok.
        """

        tempData = VolumeData(inputData)
        if tempData is not None:
            self.__rawVolume = tempData
        else:
            print('Niepoprawne dane!')
            raise ValueError

        # Stworzenie słownika z algorytmami
        self.__algorithms = {'yen-thresh': self.yenThreshSegmentation, 'region-growing':self.regionGrowingSegmentation, 'yen-region': self.yenThreshRegionSegmentation, 'otsu-iter': self.otsuIterSegmentation, 'otsu-multi': self.otsuMultiSegmentation}
    
        # Ścieżka do pliku z wynikami segmentacji
        cwd = os.getcwd()
        tempPath = cwd + '/Segmentation_' + str(datetime.datetime.now().date())
        if os.path.exists(tempPath):
            num = 1
            while True:
                tempPathNum = tempPath + '_' + str(num)
                if os.path.exists(tempPathNum):
                    num += 1
                else:
                    os.makedirs(tempPathNum)
                    self.__segmentDir = tempPathNum
                    break
        else:
            os.makedirs(tempPath)
            self.__segmentDir = tempPath

        # Inicjalizacja danych posegmentowanych
        self.__segmentedVolume = None

        # Inicjalizacja pustej nazwy algorytmu
        self.__algName = ""

    def segmentation(self, algName, params=None):
        """
        Wykonuje segmentację podanym algorytmem. Zapisuje zsegmentowane dane do pola segmentedVolume
        """
        if algName not in self.__algorithms.keys():
            print('Podano niepoprawny algorytm!')
            raise ValueError

        self.__algName = algName
        print(f'Segmentacja algorytmem {algName}.')
        if params:
            self.__segmentedVolume = self.__algorithms[algName](params)
        else:
            self.__segmentedVolume = self.__algorithms[algName]()
        
        print(f'Segmentacja algorytmem {algName} wykonana poprawnie.')

    #--------------------------------------------------------------------
    # Algorytmy - metody prywatne
    #--------------------------------------------------------------------

    def yenThreshSegmentation(self):
        """
        Wykonuje segmentację metodą Yen'a

        Wartość zwracana
            Posegmentowana macierz 3D: VolumeData
        """
        thresh = threshold_yen(self.__rawVolume.data3D)
        segVolume = self.__segmentDataByThresholds(thresh)

        return segVolume
    
    def otsuIterSegmentation(self, iterCount= 3):
        """
        Wykonuje segmentację algorytmem Otsu iteracyjnie
        Argumenty
            Słownik : iterCount: int -  Liczba iteracji algorytmu
        Wartość zwracana
            Posegmentowana macierz 3D: VolumeData
        """
        if hasattr(iterCount, "__len__"):
            if len(iterCount) != 1:
                print('Segmentacja Otsu - podano za dużo argumentów')
                raise ValueError
            else:
                iterCount = iterCount[0]    # Pierwszy element z tablicy

        if not isinstance(iterCount, int):
            iterCount = int(iterCount)

        if iterCount < 0 or iterCount > 7:
            print('Segmentacja Otsu - Liczba iteracycji musi być mniejsza od 7.')
            raise ValueError
            
        thresh = 0
        threshList = []
        for i in range(iterCount):
            thresh = self.__threshOtsu(self.__rawVolume.data3D, thresh)
            threshList.append(thresh)
        
        segVolume = self.__segmentDataByThresholds(threshList)
        print('Znalezione prgi: ', threshList)
        return segVolume
    
    def regionGrowingSegmentation(self, params=[ [0,0,0], 2, 20]):
        """
        Wykonuje segmentację algorytmem Region Growing. Za punkt startowy bierze punkt z obszaru zsegmentowantego progowaniem Otsu.
        Wartość zwracana
            Posegmentowana macierz 3D: VolumeData
        """

        img = self.__rawVolume.data3D

        trzyDe = True
        if len(img.shape) == 2:
            trzyDe = False

        startPoints, c, sigma0 = params
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

    def yenThreshRegionSegmentation(self, params=[2,20]):
        region_c, region_sigma0 = params
        img = self.__rawVolume.data3D
        thresh = threshold_yen(img)
        bw = img >= thresh
        label_image = label(bw)

        centroidy = []
        for region in regionprops(label_image):
            centroidy.append(region.centroid)

        centroidy = np.array(centroidy)
        startPoints = np.around(centroidy).astype(int)
        segImage = self.regionGrowingSegmentation([startPoints, region_c, region_sigma0])

        return segImage

    def otsuMultiSegmentation(self):
        """
        Segmentuje obraz za pomocą wielowartościowego (2) progowania Otsu.
        """
        maxVal = 256

        N = np.count_nonzero(self.__rawVolume.data3D != 0)
        hist = np.histogram(self.__rawVolume.data3D, bins=maxVal)[0]
        hist[0] = 0         # Nie uwzględnianie zera

        w0k, w1k            = 0,0      # Jakieś wagi, double
        m0k, m1k            = 0,0     # Średnie 
        thresh1, thresh2    = 0,0
        maxBetweenVar       = 0
        mt = np.sum(np.arange(maxVal) * hist / N)

        for t1 in range(maxVal):
            w0k += hist[t1] / N
            m0k += t1 * hist[t1] / N
            m0 = m0k / w0k

            w1k, m1k = 0,0
            for t2 in range(t1+1, maxVal):
                w1k += hist[t2] / N
                m1k += t2 * hist[t2] / N
                m1 = m1k / w1k
            
                w2k = 1 - (w0k + w1k)
                m2k = mt - (m0k + m1k)
                
                if w2k <= 0:
                    break
                m2 = m2k / w2k

                currVar = w0k * (m0 - mt)**2 + w1k * (m1 - mt)**2 + w2k * (m2 - mt)**2

                if maxBetweenVar < currVar:
                    maxBetweenVar = currVar
                    thresh1 = t1
                    thresh2 = t2

        thresholds = [thresh1, thresh2]
        segImage = self.__segmentDataByThresholds(thresholds)

        return segImage

    def __segmentDataByThresholds(self, ths):
        """Segmentuje obraz 2d lub 3d w odniesieniu do progów podanych jako argumenty,
        Zwraca obiekt typu VolumeData
        """

        image = self.__rawVolume.data3D
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

    def __threshOtsu(self, start_point=0):
        """
        Algorytm obliczający próg na podstawie metody Otsu.
        """
        nbins = 256 - start_point
        hist = np.histogram(self.__rawVolume.data3D, range=[start_point,255], bins=nbins)[0]
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
    # ---------------------------------------------
    # Pozostałe metody
    #----------------------------------------------

    def saveVolumeAsPickle(self, savePath = None):
        if not self.__segmentedVolume:
            print('Nie wykonano żadnej segmentacji!')
            raise NameError
            return None
        
        if savePath is None:
            savePath = self.__segmentDir + '/volumeData.pckl'
        self.__segmentedVolume.savePickle(savePath)
        print(f'Zapisano pod ścieżką: {savePath}')

    def saveSlicesAsPng(self, savePath = None):
        if not self.__segmentedVolume:
            print('Nie wykonano żadnej segmentacji!')
            raise NameError
            return None
        
        if savePath is None:
            savePath = self.__segmentDir + '/volumeSlices.png'
        self.__segmentedVolume.saveSlices(savePath, title=f'Segmentacja algorytmem {self.__algName}')
        print(f'Zapisano pod ścieżką: {savePath}')
        


    



    
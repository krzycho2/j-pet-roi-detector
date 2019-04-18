import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

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
                img3D[N-1-j,i,k] = rawData[licz,3]          # Przekopiowanie danych
                licz += 1
    
    return img3D



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
    
    def __init__(self, filePath): 
        "Tworzy obiekt na podstawie danych z pliku txt lub pickle"
        ext = os.path.splitext(filePath)[1]     # Pobranie nazwy pliku i rozszerzenia
        self._fileName = os.path.basename(os.path.normpath(filePath))
        dane = []   # Pusta macierz

        if ext == '.txt':        # Dane podane w formacie tekstowym
            print('Wykryto plik .txt')
            with open(filePath) as f:
                lines = f.readlines()
            data = []
            for s in lines:
                a = s.split()
                data.append(a)
            dane = data

        # Drugi przypadek - dane podane w formacie pickle
        elif ext == '.pckl':
            print('Wykryto plik .pickle')
            with open(filePath, 'rb') as f:
                dane = pickle.load(f)
            if is

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
        rows = 6
        cols = Nz//rows + 1
        fig = plt.figure(self._fileName)
        for index in range(0,Nz):
            ax = fig.add_subplot(rows,cols,index+1)
            ax.imshow(self.getSlice(sliceNum=index))
            ax.set_title('Slice ' + str(index))
        
        plt.show()
        


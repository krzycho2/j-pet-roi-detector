import numpy as np
import pickle
import os

# def moving_average():

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

def vol2Img3D(vol):
    """
    Konwertuje wolumem 3D z postaci N x {x,y,z,f(x,y,z)} do postaci sqrt(Nx) x sqrt(Ny) x Nz
    """
    Nz = len(np.array(list(set(vol[:,2]))))     # Zbiór unikalnych z
    N = int(np.sqrt((len(vol)/Nz)))
    
    licz = 0
    img3D = np.zeros((N,N,Nz))
    for i in range(N):
        for j in range(N):
            for k in range(Nz):
                img3D[j,i,k] = vol[licz,3]
                licz += 1
    
    return img3D

class VolumeData():
    """
    Obiekty tej klasy wykonują operacje na plikach fantoma (odczyt, zapis do pliku), które są podane jako macierz punktów liczba_punktów x {x,y,z,f} lub jako obrazy 
    """
    data3D = []
    def __init__(self, filePath): 
        "Tworzy obiekt na podstawie danych z pliku txt lub pickle"
        ext = os.path.splitext(filePath)[1]     # Pobranie rozszerzenia pliku
        if ext == '.txt':        # Dane podane w formacie tekstowym
            with open(filePath) as f:
                lines = f.readlines()
            data = []
            for s in lines:
                a = s.split()
                data.append(a)
            
            dane = np.array(data, dtype="float32")
            if len(dane[0]) == 2:               # Sprawdzenie ile wymiarów posiadają dane
                self.data3D = vol2Img3D(dane)  # Konwersja do numpy.array
            elif len(dane[0]) == 4:
                self.data3D = dane
            else:
                self = None
                print('Niepoprawny typ danych')
        
        elif ext == '.pickle':
            with open(filePath, 'rb') as f:
                pickle.load(self.data3D, f)
        
        else:
            print('Błędny typ danych')           
            self = None

    def savePickle(self, filePath = __name__ + 'Data.pckl'):    
        "Zapisuje dane jako plik pickle"
        with open(filePath, 'wb') as f:
	        pickle.dump(self.data3D, f)

    def getSlice(self, sliceNum=None, deep=None):     
        "sliceNum - numer przekroju, deep - 'głębokość w objętości podana jako liczba z przedziału (0,1)"
        if sliceNum != None and deep == None:
            return self.data3D[:,:,sliceNum]
        elif deep != None and sliceNum == None:
            sliceNum = int(deep * self.data3D.shape[2])
            return self.data3D[:,:,sliceNum]
        else:
            print('getSlice: Niepoprawna liczba argumentów')





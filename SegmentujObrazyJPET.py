"""
Główny plik projektu. Obsługuje komunikację z użytkownikiem. Można wywoływać na dwa sposoby:
- python SegmentujObrazyJPET.py - spowoduje pokazanie ekranu powitalnego i pomocy, jak używać programu
- python SegmentujObrazyJPET.py [algorytm] [plik z obrazem rekonstrukcji] [zapisać czy nie] 
"""

import sys
import os
from lib import *
from volumeData import VolumeData


def segmentuj(alg, pathToVol):
    """
    Funkcja odpowiadająca za segmentację.
    Argumenty
        alg: string - jeden z algorytmów: 'yen', 'otsu-iter', 'otsu-region'
        pathToVol: string - ścieżka do pliku z segmentacją
    Wartość zwracana
        Ścieżka do pliku z przekrojami po segmentacji
        Oprócz tego te przekroje zostaną wyświetlone
    """
    image3D = VolumeData(pathToVol)
    if image3D is None:
        print('[segmentuj] Błąd: Niepoprawna ścieżka do pliku')
        return None

    if alg == 'yen':
        segImage = image3D.yenSegment() # typ: VolumeData
    elif alg == 'otsu-iter':
        segImage = image3D.otsu_iterSegment()
    elif alg == 'otsu-region':
        image3D.otsu_regionSegment()

    # Pokazanie przekrojów po segmentacji
    slices = segImage.showAllSlicesInOne(title =f'Wynik segmentacji algorytmem  {alg}')
    
    return slices


###########################################
# PROGRAM #

# Program wywołany bez argumentów
argList = sys.argv
if len(argList) == 1:
    print('argList = 1')
    print(tekstPowitalny)

    while(True):
        polecenie = input('> ')
        userInput = polecenie.split()   # Lista członów polecenia
        if len(userInput) > 0:
            if userInput[0] == 'info':
                if len(userInput) == 2:
                    if userInput[1] == 'yen':
                        print(infoYen)
                    elif userInput[1] == 'otsu-region':
                        print(infoOtsuRegion)
                    elif userInput[1] == 'otsu-iter':
                        print(infoOtsuIter)
                    else:
                        print(infoInfo)
                else:
                    print(infoInfo)
            elif userInput[0] == 'run':
                if len(userInput) == 3:
                    if userInput[1] == 'yen' or userInput[1] == 'otsu-region' or userInput[1] == 'otsu-iter':
                        ext = os.path.splitext(userInput[2])[1]
                        if ext == '.txt' or ext == '.pckl':
                            sciezkaSegmentacja = segmentuj(*userInput[1:])
                            if sciezkaSegmentacja is not None:
                                print('Obraz z posegmentowanym wolumem został zapisany w', sciezkaSegmentacja)
                            else:
                                print('Błąd segmentacji.')
                        else:
                            print('Niepoprawne ścieżka lub rozszerzenie pliku rekonstrukcji.')
                            print(infoRun)
                    else:
                        print('Niepoprawny algorytm.')
                        print(infoRun)
                else:
                    print(infoRun)
            elif userInput[0] == 'exit':
                print('Dziękujemy za skorzystanie z programu.')
                break
            else:
                print(info)
        else:
            print(tekstPowitalny)

elif len(argList) == 3:
    if userInput[1] == 'yen' or userInput[1] == 'otsu-region' or userInput[1] == 'otsu-iter':
        ext = os.path.splitext(userInput[2])
        if ext == '.txt' or ext == '.pckl':
            segmentuj(*userInput[1:])
        else:
            print('Niepoprawne rozszerzenie pliku rekonstrukcji.')
            print(krotkieInfo)
    else:
        print('Niepoprawny algorytm.')
        print(krotkieInfo)
else:
    print('Niepoprawne wywołanie.')
    print(krotkieInfo)


"""
Główny plik projektu. Obsługuje komunikację z użytkownikiem. Można wywoływać na dwa sposoby:
- python SegmentujObrazyJPET.py - spowoduje pokazanie ekranu powitalnego i pomocy, jak używać programu
- python SegmentujObrazyJPET.py [algorytm] [plik z obrazem rekonstrukcji] [zapisać czy nie] 
"""

import sys
import os
from lib import *
from algorytmy


def segmentuj(alg, pathToVol):
    


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
                        ext = os.path.splitext(userInput[2])
                        if ext == '.txt' or ext == '.pckl':
                            segmentuj(*userInput[1:])
                        else:
                            print('Niepoprawne rozszerzenie pliku rekonstrukcji.')
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


"""
Główny plik projektu. Obsługuje komunikację z użytkownikiem. Można wywoływać na dwa sposoby:
- python SegmentujObrazyJPET.py - spowoduje pokazanie ekranu powitalnego i pomocy, jak używać programu
- python SegmentujObrazyJPET.py [algorytm] [plik z obrazem rekonstrukcji] [zapisać czy nie] 
"""

import sys
import os
from lib import *
from volumeData import VolumeData
from segmentVolume import SegmentVolume
import argparse

def _segmentuj(alg, pathToVol):
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

def main(dataPath, algName):
    seg = SegmentVolume(dataPath)


###########################################
# PROGRAM #
parser = argparse.ArgumentParser(description=TEKST_POWITALNY, formatter_class=argparse.RawDescriptionHelpFormatter)
# Argumenty obowiązkowe - algorytm i datapath
parser.add_argument('alg', metavar='ALGORITHM', type=str, help=INFO_ALG)
parser.add_argument('dataPath', metavar='PATH_TO_DATA', type=str, help=INFO_DATA)
parser.add_argument('--savePickle', action='store_true', help=INFO_SAVE_PICKLE)
parser.add_argument('--saveSlices', action='store_true', help=INFO_SAVE_SLICES)
parser.add_argument('--algParams', metavar='PARAMS_TO_PASS_TO_ALG', nargs='+')

#  metavar='SAVE_RESULT_ARRAY_TO_PICKLE',

args = parser.parse_args()
a=args._get_kwargs()
print('Podano:', args)
segObj = SegmentVolume(args.dataPath)
# segObj.saveVolumeAsPickle()
segObj.segmentation(args.alg, args.algParams)
if args.savePickle:
    segObj.saveVolumeAsPickle()   # Wydrukować ścieżkę

if args.saveSlices:
    segObj.saveSlicesAsPng()

# Program wywołany bez argumentów
"""
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
                        print(INFO_YEN)
                    elif userInput[1] == 'yen-region':
                        print(INFO_YEN_REGION)
                    elif userInput[1] == 'otsu-iter':
                        print(INFO_OTSU_ITER)
                    else:
                        print(INFO_INFO)
                else:
                    print(INFO_INFO)
            elif userInput[0] == 'run':
                if len(userInput) == 3:
                    if userInput[1] == 'yen' or userInput[1] == 'yen-region' or userInput[1] == 'otsu-iter':
                        ext = os.path.splitext(userInput[2])[1]
                        if ext == '.txt' or ext == '.pckl':
                            sciezkaSegmentacja = segmentuj(*userInput[1:])
                            if sciezkaSegmentacja is not None:
                                print('Obraz z posegmentowanym wolumem został zapisany w', sciezkaSegmentacja)
                            else:
                                print('Błąd segmentacji.')
                        else:
                            print('Niepoprawne ścieżka lub rozszerzenie pliku rekonstrukcji.')
                            print(INFO_RUN)
                    else:
                        print('Niepoprawny algorytm.')
                        print(INFO_RUN)
                else:
                    print(INFO_RUN)
            elif userInput[0] == 'exit':
                print('Dziękujemy za skorzystanie z programu.')
                break
            else:
                print(INFO)
        else:
            print(TEKST_POWITALNY)

elif len(argList) == 3:
    if userInput[1] == 'yen' or userInput[1] == 'otsu-region' or userInput[1] == 'otsu-iter':
        ext = os.path.splitext(userInput[2])
        if ext == '.txt' or ext == '.pckl':
            segmentuj(*userInput[1:])
        else:
            print('Niepoprawne rozszerzenie pliku rekonstrukcji.')
            print(KROTKIE_INFO)
    else:
        print('Niepoprawny algorytm.')
        print(KROTKIE_INFO)
else:
    print('Niepoprawne wywołanie.')
    print(KROTKIE_INFO)
"""

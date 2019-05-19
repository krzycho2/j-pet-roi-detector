"""
Główny plik projektu. Obsługuje komunikację z użytkownikiem. 
"""

from lib import *
from segmentVolume import SegmentVolume
import argparse

# Zdefinowanie parsera
parser = argparse.ArgumentParser(description=TEKST_POWITALNY, formatter_class=argparse.RawDescriptionHelpFormatter)

# Argumenty pozycyjne - algorytm i datapath
parser.add_argument('alg', metavar='ALGORITHM', type=str, help=INFO_ALG)
parser.add_argument('dataPath', metavar='PATH_TO_DATA', type=str, help=INFO_DATA)

# Argumenty opcjonalne
parser.add_argument('--savePickle', action='store_true', help=INFO_SAVE_PICKLE)
parser.add_argument('--saveSlices', action='store_true', help=INFO_SAVE_SLICES)
parser.add_argument('--algParams', metavar='PARAMS_TO_PASS_TO_ALG', nargs='+')


# Main
args = parser.parse_args()
a=args._get_kwargs()
print('Podano:', args)      # Opcjonalne
segObj = SegmentVolume(args.dataPath)
segObj.segmentation(args.alg, args.algParams)
if args.savePickle:
    segObj.saveVolumeAsPickle() 
      
if args.saveSlices:
    segObj.saveSlicesAsPng()



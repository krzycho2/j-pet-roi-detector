"""
Main script. Supports UI.
Główny plik projektu. Obsługuje komunikację z użytkownikiem 
"""

from segmentVolume import SegmentVolume
import argparse
import json

# -----Napisy wyświetlane na ekranie ---------------------------------------------------
TEKST_POWITALNY = """ Example: SegmentujObrazyJPET.py --savePickle --saveSlices --algParams='{"startPoints":[[1,1,1], [10,10,10]], "sigma0":"20", "c":"2"}' algName='yen-region' dataPath='/home/John/reconstruction.txt'
                     
                    SegmentujObrazyJPET
                by Krzysztof Krupiński 2019
 
Description
SegmentujObrazyJPET is a program for segmenting 3D volumes that originate from
PET imaging reconstruction.

The segmentation can be done using the following alogorithms:
- Yen thresholding: alg='yen-thresh', no parameters
- Iterative Otsu thresholding: alg='otsu-iter', algParams='{"iterCount":"value"}'
- Multivalue Otsu thresholding: alg='otsu-multi', no parameters
- Region Growing: alg='region-growing', algParams={"startPoints": [["x1","y1","z1"], ["x2","y2","z2"]] "region_c":value, "region_sigma0":value}'
- Region Growing using Yen threshold: alg='yen-region', algParams={"region_c":value, "region_sigma0":value}

All algorithms can be run without passing parameters. Then default parameters are acquired.

dataPath
The reconstruction image should be written to text file (.txt). A data must be formatted as a table
where following rows are: x,y,z coordinates and value correspoding to them. 
datapath="D:/Dokuments/reconstruction.txt"
"""

INFO_ALG = "Possible algorithms: yen-thresh, region-growing, yen-region, otsu-iter, otsu-multi. More info in help."

INFO_DATA = "Path to reconstruction file containg a table , where rows are: x,y,z coordinates and value correspoding to them."

INFO_SAVE_PICKLE = "Save segmented volume to pickle file."
INFO_SAVE_SLICES = "save segmentation result to png image."
INFO_PARAMS = "Namevalue parameteres that are passed to algorithms. Example: '{\"param1\": \"value1\", \"param2\": \"value2\"}.'"
# ------------- MAIN -------------------------------------------------------------------------

# Define parser
parser = argparse.ArgumentParser(description=TEKST_POWITALNY, formatter_class=argparse.RawDescriptionHelpFormatter)

# Positional arguments - algorithm i datapath
parser.add_argument('alg', metavar='ALGORITHM', type=str, help=INFO_ALG)
parser.add_argument('dataPath', metavar='PATH_TO_DATA', type=str, help=INFO_DATA)

# Optional arguments
parser.add_argument('--savePickle', action='store_true', help=INFO_SAVE_PICKLE)
parser.add_argument('--saveSlices', action='store_true', help=INFO_SAVE_SLICES)
parser.add_argument('--algParams', type=json.loads, help=INFO_PARAMS)       # json/dict arguments

# Main
args = parser.parse_args()
# print('Podano:', args)      
segObj = SegmentVolume(args.dataPath)
segObj.segmentation(args.alg, args.algParams)
if args.savePickle:
    segObj.saveVolumeAsPickle() 
      
if args.saveSlices:
    segObj.saveSlicesAsPng()



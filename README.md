# j-pet-roi-detector
Projekt dotyczący znajdowania obszarów zaintersowania (ROI) w obrazach pochodzących z tomografu PET, a konkretnie z rekonstrukcji po skanowaniu.

Segmentacja wykonywana jest następującymi metodami:
- progowanie ręczne - analityk sam dobiera progi, a następnie dzieli obraz na obsary pod względem progów(?)
- progowanie Otsu iteraycjne
- progowanie Yena
- progowanie zwykłe + Region Growing(?)

Organizacja projektu:
* Program główny i komunikacja z użytkownikiem znajduje się w pliku SegmentujObrazyJPET.py
* W pliku volumeData.py znajduje się implementacja klasy VolumeData, która odpowiada za operacje na obrazie, w tym:
  - wczytywanie obrazu z pliku tekstowego oraz pckl lub z macierzy
  - segmentacja wyżej wymienionymi algorytmami
  - wyświetlenie przekrojów obrazu
  - wyświetlenie pojedynczego przekroju
  - zapis obrazu do pliku
* W pliku lib.py znajdują się pozostałe użyteczne funkcje oraz zmienne typu string z tekstami wyświetlanymi użytkownikowi

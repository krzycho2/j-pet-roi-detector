# j-pet-roi-detector
Projekt dotyczący znajdowania obszarów zaintersowania (ROI) w obrazach pochodzących z tomografu PET, a konkoretnie z rekonstrukcji po skanowaniu.
Segmentacja wykonywana jest następującymi metodami:
- progowanie ręczne - analityk sam dobiera progi, a następnie dzieli obraz na obsary pod względem progów
- progowanie Otsu
- progowanie zwykłe + Region Growing
Stan obecny: Wykonane jest progowanie ręczne + zwykłe. Do zrobienia progowanie Otsu oraz zwykłe + Region Growing

Organizacja projektu:
* Implementacje każdego z algorytmu znajdują się w oddzielnych plikach
* każdy z algorytmów wczytuje dane z rekonstrukcji za pomocą obiektu VolumeData - implementacja znajduje się w pliku 'bibliotecznym': lib.py
* Do repozytorium nie będą wrzucane obrazy, a jedynie kody

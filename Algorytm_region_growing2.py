# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 19:39:49 2018

@author: Krzysztof Krupiński
"""
import numpy as np
import matplotlib.pyplot as plt

def srednia(_tab, _prog): # Niezbyt optymalna metoda
    suma=0
    iter=0
    [rows, columns] = _tab.shape
    if rows>0 and columns>0:
        for m in range(0, rows):
            for n in  range(0, columns):
                if _tab[m,n] > _prog:
                    suma+=_tab[m,n]
                    iter+=1
                
        sr=suma / iter
        return(sr)
    else:
        print("Niewłaściwa tablica")
    
def odch_std(_tab, _prog):
    war = srednia( (_tab - srednia(_tab, _prog) )**2, _prog)
    od_std = np.sqrt(war)
#    
    return(od_std)
                
def region_growing_by_gray_values(_tab, _prog, _c=1, _startPoint = [0, 0] ):

# startPoint przyda się później
# ̣ Tablica może być 2-D lub 3-D w ogólnosci
# c - parametr - mnoznik odchylenia standardowego we wzorze na predykat:
# M(x) = | f(x) - avg | <= c * sigma
# 

    avg=srednia(_tab, _prog)  
    sigma_c = _c * odch_std(_tab, _prog)
    [rows, columns] = _tab.shape
    nowa_tab = np.zeros([rows, columns])
    for m in range(0, rows):
        for n in range(0, columns):
            if _tab[m,n] > _prog:
                if _tab[m,n] - avg <= sigma_c:
                    nowa_tab[m,n] = _tab[m,n]
                    
    return(nowa_tab)
                    


"""
PRZYKLADOWE DANE. Dla ulatwienia przyklad 2D, ale zaden problem dolozyc 3. wymiar.

Tło to szum, zakładamy, że o wiele słabsze od wartosci 
szukanego obszaru.
"""

tabliczka = np.random.randint(10, size = (5, 5))
tabliczka[3,0] = 200
tabliczka[3,1] = 210
tabliczka[4,0] = 190
tabliczka[4,1] = 200

prog = 100
#print(tabliczka)

# (n, bins) = np.histogram(tabliczka)
# prog = np.argmin(n) 
# Z tym własnie nie mogłem sobie poradzić:
# Jak odczytać z histogramu odciętą - czyli szukany próg.

tab = region_growing_by_gray_values(tabliczka, prog)
print(tab)
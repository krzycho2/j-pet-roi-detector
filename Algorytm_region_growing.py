# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 19:39:49 2018

@author: Krzysztof Krupiński
"""
import numpy as np
import matplotlib.pyplot as plt

def srednia(tab, prog): # Niezbyt optymalna metoda
    suma=0
    iter=0
    [rows, columns] = tab.shape
    for m in range(0, rows-1):
        for n in range(0, columns):
            if tab[m,n] > prog:
                suma+=tab[m,n]
                iter+=1
                
    sr=suma / iter
    return(sr)
    
def odch_std(tab, prog):
    ...
                
def region_growing_by_gray_values(tablica, startingPoint = [0, 0], c, threshold):

""" Tablica może być 2-D lub 3-D w ogólnosci
c - parametr - mnoznik odchylenia standardowego we wzorze na predykat:
M(x) = | f(x) - avg | <= c * sigma

"""
    avg=srednia(tablica, threshold)  
    sigma_c = c * odch_std(tablica, threshold)
    [rows, columns] = tablica.shape
    nowa_tablica = np.zeros([rows, columns])
    for m in range(0, rows-1):
        for n in range(0, columns):
            if tablica[m,n] > threshold:
                if tablica[m,n] - avg <= sigma_c:
                    nowa_tablica[m,n] = tablica[m,n]
                    
    return(nowa_tablica)
                    


"""
PRZYKLADOWE DANE. Dla ulatwienia przyklad 2D, ale zaden problem dolozyc 3. wymiar.

Tło to szum, zakładamy, że o wiele słabsze od wartosci 
szukanego obszaru.
"""

tabliczka = 10 * np.random.rand(5,5)
tabliczka[3,0] = 200
tabliczka[3,1] = 210
tabliczka[4,0] = 190
tabliczka[4,1] = 200
#print(tabliczka)

(n, bins) = np.histogram(tabliczka)
prog = np.argmin(n) # Z tym własnie nie mogłem sobie poradzić:
# Jak odczytać z histogramu odciętą - czyli szukany próg.




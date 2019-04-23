import numpy as np
import matplotlib.pyplot as plt
import pickle
from lib import VolumeData, getListOfFiles


# Wymagamy, żeby dane były w formacie uint8
path = '/home/krzysztof/Dokumenty/Praca_inż/j-pet-roi-detector/fantomNowy.pckl'
vol = VolumeData(path)

slice75 = vol.getSlice(sliceNum=75)
slice75 = np.array(255 * slice75, dtype='uint8')

# Histogram
maxVal = 256
# N = 0 # Licznik niezerowych punktów
# hist = np.zeros(maxVal)
h, w = slice75.shape 
# for i in range(h):
#     for j in range(w):
#         val = slice75[i,j]
#         if val != 0:
#             hist[val] += 1
#             N += 1

hist = np.histogram(slice75, bins=maxVal)[0]
N = h*w
w0k, w1k, w2k   = 0,0,0       # Jakieś wagi, double
m0k, m1k, n2k   = 0,0,0
m0, m1, m2      = 0,0,0
m0k, m1k, mt    = 0,0,0
currVar         = 0
thresh1, thresh2= 0,0
maxBetweenVar   = 0

for k in range(maxVal):
    mt += k * hist[k] / N

plt.plot(np.arange(256), hist)
plt.show()


for t1 in range(maxVal):
    w0k += hist[t1] / N
    m0k += t1 * hist[t1] / N
    m0 = m0k / w0k
    # print(f't1: {t1}, hist[t1]: {hist[t1]}, w0k: {w0k}, m0k: {m0k}, m0: {m0}')

    w1k, m1k = 0,0
    for t2 in range(t1+1, maxVal):
        w1k += hist[t2] / N
        m1k += t2 * hist[t2] / N
        m1 = m1k / w1k
        # print(f'    t2: {t2}, hist[t2]: {hist[t2]}, w1k: {w1k}, m1k: {m1k}, m1: {m1}')

        w2k = 1 - (w0k + w1k)
        m2k = mt - (m0k + m1k)
        
        if w2k <= 0:
            # print('w2k < 0')
            break
        m2 = m2k / w2k
        # print(f'    w2k: {w2k}, m2k: {m2k}, m2: {m2}')

        currVar = w0k * (m0 - mt)**2 + w1k * (m1 - mt)**2 + w2k * (m2 - mt)**2
        # print(f'    currVar: {currVar}')

        if maxBetweenVar < currVar:
            maxBetweenVar = currVar
            thresh1 = t1
            thresh2 = t2

# Przyporządkowanie punktów do trzech klas
# red = np.zeros(slice75.shape); grn = r; blu = r
segData = np.zeros((*slice75.shape, 3), dtype='uint8')
for i in range(h):
    for j in range(w):
        if slice75[i,j] < thresh1:
            segData[i,j] = 255,0,0
        elif slice75[i,j] >= thresh1 and slice75[i,j] < thresh2:
            segData[i,j] = 0,255,0
        else:
            segData[i,j] = 0,0,255

# red = slice75 < thresh1
# grn = (slice75 >= thresh1); grn = slice75 < thresh2)
# blu = slice75 >= thresh2

# segData = 255* np.array((red,grn,blu), dtype='uint8'
plt.subplot(1,2,1); plt.imshow(slice75); plt.title('Obraz oryginalny')
plt.subplot(1,2,2); plt.imshow(segData); plt.title('Obraz po segmentacji metodą Otsu dwuwartościową')
plt.show()



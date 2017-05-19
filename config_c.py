import numpy as np
import ctypes as ct

epalib = ct.cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')
biHourToYear = float(.0002283105022831050228310502283105)
biHour = 0
data = {'real':{'iron':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pvc':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pump':{'tH':[], 'age':[], 'fS':[], 'index':[]}}, 'noTemp': {'iron':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pvc':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pump':{'tH':[], 'age':[], 'fS':[], 'index':[]}}, 'noTime': {'iron':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pvc':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pump':{'tH':[], 'age':[], 'fS':[], 'index':[10, 335]}}}

tasFile = open('D:\\Austin_Michne\\1_11_17\\tasMaxBD.txt', 'r')
tasList = tasFile.read().expandtabs().splitlines()
tasFile.close()
tasMaxACTList = {'real': list(tasList), 'noTime': list(tasList), 'noTemp': list(np.repeat([22], 33000))}

f = open('north_marin_c.inp', 'r')
fi = open('D:\\Austin_Michne\\tripleSim\\zz.rpt', 'w')

# Initializes the files for encoding
a = 'north_marin_c.inp'
b = 'D:\\Austin_Michne\\tripleSim\\zz.rpt'

# Byte objects
b_a = a.encode('UTF-8')
b_b = b.encode('UTF-8')

epalib.ENopen(b_a, b_b, "")
epalib.ENopenH()
timestep = ct.pointer(ct.c_long(7200))
time = ct.pointer(ct.c_long(0))
init_flag = ct.c_int(1)
epalib.ENinitH(init_flag)

nodeCount = ct.pointer(ct.c_int(0))
epalib.ENgetcount(ct.c_int(0), nodeCount)
nodeValue = ct.pointer(ct.c_float(0.0))
nodeID = ct.c_char_p(('Testing purposes').encode('UTF-8'))

linkList = ct.pointer(ct.c_int(0))
epalib.ENgetcount(ct.c_int(0), linkList)
linkCounter = 0
currentRough = ct.pointer(ct.c_float(0.0))

while (linkCounter < linkList.contents.value):
    epalib.ENgetlinkvalue(ct.c_int(linkCounter), ct.c_int(2), currentRough)
    if (currentRough.contents.value > 140):
        randironAge = np.random.uniform(0, 85, 1)
        data['real']['iron']['age'].append(randironAge)
        data['noTemp']['iron']['age'].append(randironAge)
        data['noTime']['iron']['age'].append(65)

        data['real']['iron']['fS'].append(0)
        data['noTemp']['iron']['fS'].append(0)
        data['noTime']['iron']['fS'].append(0)

        tH = np.random.uniform(0, 1, 1)
        data['real']['iron']['tH'].append(tH)
        data['noTemp']['iron']['tH'].append(tH)
        data['noTime']['iron']['tH'].append(tH)

        data['real']['iron']['index'].append(linkList.contents)
        data['noTemp']['iron']['index'].append(linkList.contents)
        data['noTime']['iron']['index'].append(linkList.contents)

    elif (currentRough.contents.value < 140):
        if (linkCounter > 20):
            randpvcAge = np.random.uniform(40, 9, 1)
        else:
            randpvcAge = np.random.normal(13, 3, 1)

        data['real']['pvc']['age'].append(randpvcAge)
        data['noTemp']['pvc']['age'].append(randpvcAge)
        data['noTime']['pvc']['age'].append([65])

        data['real']['pvc']['fS'].append(0)
        data['noTemp']['pvc']['fS'].append(0)
        data['noTime']['pvc']['fS'].append(0)

        tH = np.random.uniform(0, 1, 1)
        data['real']['pvc']['tH'].append(tH)
        data['noTemp']['pvc']['tH'].append(tH)
        data['noTime']['pvc']['tH'].append(tH)

        data['real']['pvc']['index'].append(linkList.contents)
        data['noTemp']['pvc']['index'].append(linkList.contents)
        data['noTime']['pvc']['index'].append(linkList.contents)

    linkCounter += 1

data['real']['pump']['age'] = [10, 25]
data['noTime']['pump']['age'] = [10, 25]
data['noTime']['pump']['age'] = [10, 25]

tH = np.random.uniform(0, 1, 2)
data['real']['pump']['tH'] = list(tH)
data['noTemp']['pump']['tH'] = list(tH)
data['noTime']['pump']['tH'] = list(tH)

data['real']['pump']['fS'] = [0, 0]
data['noTemp']['pump']['fS'] = [0, 0]
data['noTime']['pump']['fS'] = [0, 0]

pvcWeibullFile = open('D:\\Austin_Michne\\1_11_17\\pvcWeibullFixed.txt', 'r')
pvcWeibullList = pvcWeibullFile.read().splitlines()
pvcWeibullFile.close()

ironWeibullFile = open('D:\\Austin_Michne\\1_11_17\\ironWeibullFixed.txt', 'r')
ironWeibullList = ironWeibullFile.read().splitlines()
ironWeibullFile.close()

pumpWeibullFile = open('D:\\Austin_Michne\\1_11_17\\pumpWeibullFixed.txt', 'r')
pumpWeibullList = pumpWeibullFile.read().splitlines()
pumpWeibullFile.close()


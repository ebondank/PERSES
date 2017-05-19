import numpy as np
import ctypes as ct
import parent_c


biHourToYear = float(.0002283105022831050228310502283105)
biHour = 0
data = {'real':{'iron':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pvc':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pump':{'tH':[], 'age':[], 'fS':[], 'index':['10', '335']}}, 'noTemp': {'iron':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pvc':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pump':{'tH':[], 'age':[], 'fS':[], 'index':['10', '335']}}, 'noTime': {'iron':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pvc':{'tH':[], 'age':[], 'fS':[], 'index':[]}, 'pump':{'tH':[], 'age':[], 'fS':[], 'index':[10, 335]}}}

tasFile = open('D:\\Austin_Michne\\1_11_17\\tasMaxBD.txt', 'r')
tasList = tasFile.read().expandtabs().splitlines()
tasFile.close()
tasMaxACTList = {'real': list(tasList), 'noTime': list(tasList), 'noTemp': list(np.repeat([22], 33000))}

linkList = ct.pointer(ct.c_int(0))
parent_c.epalib.ENgetcount(ct.c_int(0), linkList)
linkCounter = 0
currentRough = ct.pointer(ct.c_float(0.0))

while (linkCounter < linkList.contents.value):
    parent_c.epalib.ENgetlinkvalue(ct.c_int(2), currentRough)
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
        data['noTime']['pvc']['age'].append(65)

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


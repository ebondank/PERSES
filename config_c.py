import numpy as np
import ctypes as ct

epalib = ct.cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')
biHourToYear = float(.0002283105022831050228310502283105)
biHour = 0
data = {'real':{'iron':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}, 'pvc':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}, 'pump':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}}, 'noTemp': {'iron':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}, 'pvc':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}, 'pump':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}}, 'noTime': {'iron':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}, 'pvc':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}, 'pump':{'tH':list(), 'age':list(), 'fS':list(), 'index':list()}}}

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
printItem = str

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

#TODO
indexReturn = ct.pointer(ct.c_int(0))
linkID = ct.c_wchar_p('10')
epalib.ENgetlinkindex(linkID, indexReturn)
indexReturn = indexReturn.contents.value
data['real']['pump']['index'].append(indexReturn)
data['noTemp']['pump']['index'].append(indexReturn)
data['noTime']['pump']['index'].append(indexReturn)
linkID = ct.c_wchar_p('335')
indexReturn = ct.pointer(ct.c_int(0))
epalib.ENgetlinkindex(linkID, indexReturn)
indexReturn = indexReturn.contents.value
data['real']['pump']['index'].append(indexReturn)
data['noTemp']['pump']['index'].append(indexReturn)
data['noTime']['pump']['index'].append(indexReturn)

while (linkCounter < linkList.contents.value):
    epalib.ENgetlinkvalue(ct.c_int(linkCounter), ct.c_int(2), currentRough)
    if (currentRough.contents.value > 140):
        randironAge = float(np.random.uniform(0, 85, 1))
        data['real']['iron']['age'].append(randironAge)
        data['noTemp']['iron']['age'].append(randironAge)
        data['noTime']['iron']['age'].append(65)

        data['real']['iron']['fS'].append(0)
        data['noTemp']['iron']['fS'].append(0)
        data['noTime']['iron']['fS'].append(0)

        tH = float(np.random.uniform(0, 1, 1))
        data['real']['iron']['tH'].append(tH)
        data['noTemp']['iron']['tH'].append(tH)
        data['noTime']['iron']['tH'].append(tH)

        data['real']['iron']['index'].append(linkList.contents)
        data['noTemp']['iron']['index'].append(linkList.contents)
        data['noTime']['iron']['index'].append(linkList.contents)

    elif (currentRough.contents.value < 140):
        if (linkCounter > 20):
            randpvcAge = float(np.random.uniform(40, 9, 1))
        else:
            randpvcAge = float(np.random.normal(13, 3, 1))

        data['real']['pvc']['age'].append(randpvcAge)
        data['noTemp']['pvc']['age'].append(randpvcAge)
        data['noTime']['pvc']['age'].append(65)

        data['real']['pvc']['fS'].append(0)
        data['noTemp']['pvc']['fS'].append(0)
        data['noTime']['pvc']['fS'].append(0)

        tH = float(np.random.uniform(0, 1, 1))
        data['real']['pvc']['tH'].append(tH)
        data['noTemp']['pvc']['tH'].append(tH)
        data['noTime']['pvc']['tH'].append(tH)

        data['real']['pvc']['index'].append(linkList.contents)
        data['noTemp']['pvc']['index'].append(linkList.contents)
        data['noTime']['pvc']['index'].append(linkList.contents)

    linkCounter += 1

data['real']['pump']['age'] = list([10, 25])
data['noTime']['pump']['age'] = list([10, 25])
data['noTime']['pump']['age'] = list([10, 25])

tH1 = float(np.random.uniform(0, 1, 1))
tH2 = float(np.random.uniform(0, 1, 1))
data['real']['pump']['tH'] = [tH1, tH2]
data['noTemp']['pump']['tH'] = [tH1, tH2]
data['noTime']['pump']['tH'] = [tH1, tH2]

data['real']['pump']['fS'] = list([0, 0])
data['noTemp']['pump']['fS'] = list([0, 0])
data['noTime']['pump']['fS'] = list([0, 0])

pvcWeibullFile = open('D:\\Austin_Michne\\1_11_17\\pvcWeibullFixed.txt', 'r')
pvcWeibullList = pvcWeibullFile.read().splitlines()
pvcWeibullFile.close()

ironWeibullFile = open('D:\\Austin_Michne\\1_11_17\\ironWeibullFixed.txt', 'r')
ironWeibullList = ironWeibullFile.read().splitlines()
ironWeibullFile.close()

pumpWeibullFile = open('D:\\Austin_Michne\\1_11_17\\pumpWeibullFixed.txt', 'r')
pumpWeibullList = pumpWeibullFile.read().splitlines()
pumpWeibullFile.close()


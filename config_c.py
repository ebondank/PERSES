import numpy as np
import ctypes as ct

epalib = ct.cdll.LoadLibrary('epanet2mingw64.dll')
biHourToYear = float(.0002283105022831050228310502283105)
biHour = 0
data = {'real':{'iron':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pvc':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pump':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}}, 'noTemp': {'iron':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pvc':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pump':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}}, 'noTime_yesCC': {'iron':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pvc':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pump':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}}, 'noTime_noCC': {'iron':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pvc':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}, 'pump':{'ctH':list(), 'ltH': list(), 'age':list(), 'fS':list(), 'index':list()}}}

normal_run_list = [list()]*24

tasFile = open('generatedTasMaxBD85.txt', 'r')
tasList = tasFile.read().expandtabs().splitlines()
tasFile.close()

histTasFile = open('generatedTasMaxHist.txt', 'r')
histTasList = histTasFile.read().expandtabs().splitlines()
histTasFile.close()
tasMaxACTList = {'real': list(tasList), 'noTime_yesCC': list(tasList), 'noTime_noCC': list(histTasList), 'noTemp': list(histTasList)}

f = open('north_marin_c.inp', 'r')
fi = open('placeholder.rpt', 'w')

# Initializes the files for encoding
a = 'north_marin_c.inp'
b = 'placeholder.rpt'

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
epalib.ENgetcount(ct.c_int(2), linkList)
linkCounter = 1
currentRough = ct.pointer(ct.c_float(0.0))


# TODO Right now the config for failure is to fail between pump && node, not reservoir && pump
# int appended to list from int pointer return of 'ENgetlinkindex'
indexReturn1 = ct.pointer(ct.c_int(0))
# For the first pipe out of pump 10
linkID = ct.c_char_p(str(10).encode('utf-8'))
epalib.ENgetlinkindex(linkID, indexReturn1)
data['real']['pump']['index'].append(indexReturn1.contents)
data['noTemp']['pump']['index'].append(indexReturn1.contents)
data['noTime_yesCC']['pump']['index'].append(indexReturn1.contents)
data['noTime_noCC']['pump']['index'].append(indexReturn1.contents)
# For the first pipe out of pump 335
linkID = ct.c_char_p(str(335).encode('utf-8'))
indexReturn2 = ct.pointer(ct.c_int(0))
epalib.ENgetlinkindex(linkID, indexReturn2)
data['real']['pump']['index'].append(indexReturn2.contents)
data['noTemp']['pump']['index'].append(indexReturn2.contents)
data['noTime_yesCC']['pump']['index'].append(indexReturn2.contents)
data['noTime_noCC']['pump']['index'].append(indexReturn2.contents)

# Roughness look to determine pipe type
# Using pure c integers in the lists
while (linkCounter < linkList.contents.value):
    indexVal = ct.c_int(linkCounter)
    epalib.ENgetlinkvalue(indexVal, ct.c_int(2), currentRough)
    # Filtering the pumps
    if linkCounter != (indexReturn1.contents.value or indexReturn2.contents.value):
        if (int(currentRough.contents.value) > 140):
            randironAge = float(np.random.uniform(0, 72, 1)[0])
            data['real']['iron']['age'].append(randironAge)
            data['noTemp']['iron']['age'].append(randironAge)
            data['noTime_yesCC']['iron']['age'].append(55)
            data['noTime_noCC']['iron']['age'].append(55)

            data['real']['iron']['fS'].append(0)
            data['noTemp']['iron']['fS'].append(0)
            data['noTime_yesCC']['iron']['fS'].append(0)
            data['noTime_noCC']['iron']['fS'].append(0)

            ltH = list(np.random.uniform(0, 1, 50))
            ctH = float(ltH[0])
            data['real']['iron']['ltH'].append(ltH)
            data['real']['iron']['ctH'].append(ctH)
            data['noTemp']['iron']['ltH'].append(ltH)
            data['noTemp']['iron']['ctH'].append(ctH)
            data['noTime_yesCC']['iron']['ltH'].append(ltH)
            data['noTime_yesCC']['iron']['ctH'].append(ctH)
            data['noTime_noCC']['iron']['ltH'].append(ltH)
            data['noTime_noCC']['iron']['ctH'].append(ctH)

            data['real']['iron']['index'].append(indexVal)
            data['noTemp']['iron']['index'].append(indexVal)
            data['noTime_yesCC']['iron']['index'].append(indexVal)
            data['noTime_noCC']['iron']['index'].append(indexVal)

        elif (int(currentRough.contents.value) < 140):
            if (linkCounter > 20):
                randpvcAge = float(np.random.uniform(27, 6, 1)[0])
            else:
                randpvcAge = float(np.random.normal(13, 3, 1)[0])

            data['real']['pvc']['age'].append(randpvcAge)
            data['noTemp']['pvc']['age'].append(randpvcAge)
            data['noTime_yesCC']['pvc']['age'].append(47)
            data['noTime_noCC']['pvc']['age'].append(47)

            data['real']['pvc']['fS'].append(0)
            data['noTemp']['pvc']['fS'].append(0)
            data['noTime_yesCC']['pvc']['fS'].append(0)
            data['noTime_noCC']['pvc']['fS'].append(0)

            ltH = list(np.random.uniform(0, 1, 50))
            ctH = float(ltH[0])
            data['real']['pvc']['ltH'].append(ltH)
            data['real']['pvc']['ctH'].append(ctH)
            data['noTemp']['pvc']['ltH'].append(ltH)
            data['noTemp']['pvc']['ctH'].append(ctH)
            data['noTime_yesCC']['pvc']['ltH'].append(ltH)
            data['noTime_yesCC']['pvc']['ctH'].append(ctH)
            data['noTime_noCC']['pvc']['ltH'].append(ltH)
            data['noTime_noCC']['pvc']['ctH'].append(ctH)

            data['real']['pvc']['index'].append(indexVal)
            data['noTemp']['pvc']['index'].append(indexVal)
            data['noTime_yesCC']['pvc']['index'].append(indexVal)
            data['noTime_noCC']['pvc']['index'].append(indexVal)

    linkCounter += 1

data['real']['pump']['age'] = list([4, 6])
data['noTemp']['pump']['age'] = list([4, 6])
data['noTime_yesCC']['pump']['age'] = list([5.5, 5.25])
data['noTime_noCC']['pump']['age'] = list([5.5, 5.25])

ltH1 = list(np.random.uniform(0, 1, 5000))
ctH1 = float(ltH1[0])
ltH2 = list(np.random.uniform(0, 1, 5000))
ctH2 = float(ltH2[0])
data['real']['pump']['ltH'] = [ltH1, ltH2]
data['real']['pump']['ctH'] = [ctH1, ctH2]
data['noTemp']['pump']['ltH'] = [ltH1, ltH2]
data['noTemp']['pump']['ctH'] = [ctH1, ctH2]
data['noTime_yesCC']['pump']['ltH'] = [ltH1, ltH2]
data['noTime_yesCC']['pump']['ctH'] = [ctH1, ctH2]
data['noTime_noCC']['pump']['ltH'] = [ltH1, ltH2]
data['noTime_noCC']['pump']['ctH'] = [ctH1, ctH2]

data['real']['pump']['fS'] = list([0, 0])
data['noTemp']['pump']['fS'] = list([0, 0])
data['noTime_yesCC']['pump']['fS'] = list([0, 0])
data['noTime_noCC']['pump']['fS'] = list([0, 0])

pvcWeibullFile = open('pvcWeibullFixed.txt', 'r')
pvcWeibullList = pvcWeibullFile.read().splitlines()
pvcWeibullFile.close()

ironWeibullFile = open('ironWeibullFixed.txt', 'r')
ironWeibullList = ironWeibullFile.read().splitlines()
ironWeibullFile.close()

pumpWeibullFile = open('pumpWeibullFixed.txt', 'r')
pumpWeibullList = pumpWeibullFile.read().splitlines()
pumpWeibullFile.close()
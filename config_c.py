import os
import math
import numpy as np
import ctypes as ct

epalib = ct.cdll.LoadLibrary('epanet2mingw64.dll')
biHourToYear = float(.0002283105022831050228310502283105)
normal_run_list = [list()]*24
tasMaxACTList = dict()
biHour = 0

pipe_attributes = {'ctH':list(), 'ltH': list(), 'exp':list(), 'fS':list(), 'index':list(), 'prob': list()}
pump_attributes = {'motor_ctH':list(), 'elec_ctH':list(), 'motor_ltH': list(), 'elec_ltH': list(), 'motor_exp': list(),'elec_exp':list(), 'fS':list(), 'index':list(), 'prob': list()}
threeSim = {'iron': pipe_attributes, 'pvc': pipe_attributes, 'pump': pump_attributes}
data = {'real':threeSim, 'noTemp': threeSim, 'historical': threeSim}

tempFileList = {'real': 'hist85.txt', \
                'noTime_noCC': 'hist45.txt', \
                'noTemp':'hist45.txt', \
                'historical': 'histTasMaxBD.txt'}
for key in tempFileList:
    with open(tempFileList[key], 'r') as f_:
        tasMaxACTList[key] = f_.read().expandtabs().splitlines() 

with open('north_marin_c.inp', 'r') as f, open('placeholder.rpt', 'w') as fi:
    # Initializes the files for encoding
    # Byte objects
    a = 'north_marin_c.inp'; b_a = a.encode('UTF-8')
    b = 'placeholder.rpt'; b_b = b.encode('UTF-8')
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

    indexReturn1 = ct.pointer(ct.c_int(0))
    # For the first pipe out of pump 10
    linkID = ct.c_char_p(str(10).encode('utf-8'))
    epalib.ENgetlinkindex(linkID, indexReturn1)
    # For the first pipe out of pump 335
    linkID = ct.c_char_p(str(335).encode('utf-8'))
    indexReturn2 = ct.pointer(ct.c_int(0))
    epalib.ENgetlinkindex(linkID, indexReturn2)
    for key in data:
        data[key]['pump']['index'].append(indexReturn1.contents)
        data[key]['pump']['index'].append(indexReturn2.contents)

    # Roughness look to determine pipe type
    # Using pure c integers in the lists
    while (linkCounter < linkList.contents.value):
        indexVal = ct.c_int(linkCounter)
        epalib.ENgetlinkvalue(indexVal, ct.c_int(2), currentRough)
        if linkCounter != (indexReturn1.contents.value or indexReturn2.contents.value):
            if (int(currentRough.contents.value) > 140):
                for key in data:
                    data[key]['iron']['index'].append(indexVal)
            elif (int(currentRough.contents.value) < 140):
                for key in data:
                    data[key]['pvc']['index'].append(indexVal)
        linkCounter += 1

pvc_count = len(data[key]['pvc']['index'])
iron_count = len(data[key]['iron']['index'])
pump_count = len(data[key]['pump']['index'])
for key in data:
    data[key]['pvc']['exp'] = [0]*pvc_count
    data[key]['iron']['exp'] = [0]*iron_count
    data[key]['pvc']['ltH'] = np.random.rand(pvc_count, 100).tolist()
    data[key]['iron']['ltH'] = np.random.rand(iron_count, 100).tolist()
    data[key]['pvc']['fS'] = [0]*pvc_count
    data[key]['iron']['fS'] = [0]*iron_count
    for value in data[key]['iron']['ltH']:
        data[key]['iron']['ctH'].append(value[0])
    for value in data[key]['pvc']['ltH']:
        data[key]['pvc']['ctH'].append(value[0])

    data[key]['pump']['motor_exp'] = [0]*pump_count
    data[key]['pump']['elec_exp'] = [0]*pump_count
    data[key]['pump']['motor_ltH'] = np.random.rand(pump_count, 100).tolist()
    data[key]['pump']['elec_ltH'] = np.random.rand(pump_count, 100).tolist()
    data[key]['pump']['fS'] = [0]*pump_count
    for value in data[key]['pump']['motor_ltH']:
        data[key]['pump']['motor_ctH'].append(value[0])
        data[key]['pump']['elec_ctH'].append(value[0])


with open(os.path.relpath('new_cdf\\pvc_made_cdf.txt'), 'r') as pvc_exp_f:
    pvc_exp_list = pvc_exp_f.read().splitlines()
with open(os.path.relpath('new_cdf\\iron_made_cdf.txt'), 'r') as iron_exp_f:
    iron_exp_list = iron_exp_f.read().splitlines()
with open(os.path.relpath('new_cdf\\elec_made_cdf.txt'), 'r') as elec_exp_f, \
     open(os.path.relpath('new_cdf\\motor_made_cdf.txt'), 'r') as motor_exp_f:
    elec_exp_list = elec_exp_f.read().splitlines()
    motor_exp_list = motor_exp_f.read().splitlines()
distList = {'motor': motor_exp_list, 'elec': elec_exp_list, 'pvc': pvc_exp_list, 'iron': iron_exp_list}
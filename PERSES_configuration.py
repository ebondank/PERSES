import os
import math
import numpy as np
import ctypes as ct

biHourToYear = float(.0002283105022831050228310502283105)
normal_run_list = [list()]*24
tasMaxACTList = dict()
biHour = 0

# Current Threshold, List of Thresholds, Exposure, Failure Status, Index
class pipe_attributes(object):
    def __init__(self):
        self.prop = {'ctH':list(), 'ltH': list(), 'exp':list(), 'fS':list(), 'index':list()}


# Motors Current Threshold,Electronics current threshold, List of Thresholds for both, Exposure for both, Failure Status, Index
class pump_attributes(object):
    def __init__(self):
        self.prop = {'motor_ctH':list(), 'elec_ctH':list(), 'motor_ltH': list(), \
            'elec_ltH': list(), 'motor_exp': list(),'elec_exp':list(), 'fS':list(), 'index':list()}

class simulation_creation(object):
    def __init__(self):
        self.sim = dict()
    def sims_to_run(self, simulation_dict):
        for key in simulation_dict.keys():
            self.sim[key] = dict()
            self.sim[key]["epanet"] = ct.cdll.LoadLibrary('epanet2.dll')
            for component_type in simulation_dict[key]:
                if 'pump' in component_type:
                    self.sim[key][component_type] = pump_attributes().prop
                else:
                    self.sim[key][component_type] = pipe_attributes().prop
        return self.sim
epalib = ct.cdll.LoadLibrary('epanet2.dll')
comps = ['pump', 'iron', 'pvc']
sim_list = {'temp_curves': ['rcp85', 'rcp45', 'historical'],\
                 'rep_times': [{'pipe':22, 'pump':4}, {'pipe':44, 'pump':8}, {'pipe':88, 'pump':16}]}
sim_list_strings = list()
for temp in sim_list['temp_curves']:
    for rep in sim_list['rep_times']:
        sim_list_strings.append(("{}_{}_{}").format(temp, rep['pipe'], rep['pump']))

sims_struct_gen_dict = dict()
for sim in sim_list_strings:
    sims_struct_gen_dict[sim] = comps
data = simulation_creation().sims_to_run(sims_struct_gen_dict)

# Temperature files, there are available in the github repo
if os.name == "nt":
    tempFileList = {'rcp85': 'rcp85_1950_2100.txt', \
                    # 'noTime_noCC': 'hist45.txt', \
                    'rcp45':'rcp45_1950_2100.txt', \
                    'historical': 'hist_2100.txt'}
else:
    tempFileList = {'rcp85': 'rcp85_1950_2100.txt', \
                    # 'noTime_noCC': 'hist45.txt', \
                    'rcp45':'rcp45_1950_2100.txt', \
                    'historical': 'hist_2100.txt'}
for key in tempFileList:
    with open(tempFileList[key], 'r') as f_:
        tasMaxACTList[key] = f_.read().expandtabs().splitlines() 

# Sample input network, finding pumps in a network is a pain so I hardcoded that portion
with open('north_marin_c.inp', 'r') as f, open('placeholder.rpt', 'w') as fi:
    # Initializes the files for encoding and creates their byte objects
    a = 'north_marin_c.inp'; b_a = a.encode('UTF-8')
    b = 'placeholder.rpt'; b_b = b.encode('UTF-8')
    epalib.ENopen(b_a, b_b, "")
    epalib.ENopenH()
    timestep = ct.pointer(ct.c_long(7200))
    time = ct.pointer(ct.c_long(0))
    init_flag = ct.c_int(1)
    epalib.ENinitH(init_flag)
    # Getting network statistics
    nodeCount = ct.pointer(ct.c_int(0))
    epalib.ENgetcount(ct.c_int(0), nodeCount)
    nodeValue = ct.pointer(ct.c_float(0.0))
    nodeID = ct.c_char_p(('Testing purposes').encode('UTF-8'))
    # Getting the list of links
    linkList = ct.pointer(ct.c_int(0))
    epalib.ENgetcount(ct.c_int(2), linkList)
    linkCounter = 1
    currentRough = ct.pointer(ct.c_float(0.0))
    # Seperating the link population based on roughness
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
        data[sim_list_strings[0]]['epanet'].ENgetlinkvalue(indexVal, ct.c_int(2), currentRough)
        if linkCounter != (indexReturn1.contents.value or indexReturn2.contents.value):
            if (int(currentRough.contents.value) > 140):
                for key in data:
                    data[key]['iron']['index'].append(indexVal)
            elif (int(currentRough.contents.value) < 140):
                for key in data:
                    data[key]['pvc']['index'].append(indexVal)
        linkCounter += 1

# Setting fixed distributions to ensure synchrony across simulations
# Extremely important if attemping to compare simulations based on isolated variable changes
pvc_count = len(data[key]['pvc']['index'])
iron_count = len(data[key]['iron']['index'])
pump_count = len(data[key]['pump']['index'])
motor_ltH = list()
elec_ltH = list()
pvc_ltH = list()
iron_ltH = list()
for i in range(0, pump_count):
    motor_ltH.append(np.random.random(100).tolist())
    elec_ltH.append(np.random.random(100).tolist())
for i in range(0, pvc_count): pvc_ltH.append(np.random.random(100).tolist())
for i in range(0, iron_count): iron_ltH.append(np.random.random(100).tolist())

# Setting component level attributes for everything in the current simulation set
for key in data:
    data[key]['pvc']['exp'] = [0]*pvc_count
    data[key]['iron']['exp'] = [0]*iron_count
    data[key]['pvc']['ltH'] = pvc_ltH
    data[key]['iron']['ltH'] = iron_ltH
    data[key]['pvc']['fS'] = [0]*pvc_count
    data[key]['iron']['fS'] = [0]*iron_count
    for value in data[key]['iron']['ltH']:
        data[key]['iron']['ctH'].append(value[0])
    for value in data[key]['pvc']['ltH']:
        data[key]['pvc']['ctH'].append(value[0])

    data[key]['pump']['motor_exp'] = [0]*pump_count
    data[key]['pump']['elec_exp'] = [0]*pump_count
    data[key]['pump']['motor_ltH'] = motor_ltH
    data[key]['pump']['elec_ltH'] = elec_ltH
    data[key]['pump']['fS'] = [0]*pump_count
    for value in data[key]['pump']['motor_ltH']:
        data[key]['pump']['motor_ctH'].append(value[0])
    for value in data[key]['pump']['elec_ltH']:
        data[key]['pump']['elec_ctH'].append(value[0])

# Adding in the exposure files, which are loosely relatable to a CDF
with open(os.path.relpath('new_cdf\\pvc_made_cdf.txt'), 'r') as pvc_exp_f:
    pvc_exp_list = pvc_exp_f.read().splitlines()
with open(os.path.relpath('new_cdf\\iron_made_cdf.txt'), 'r') as iron_exp_f:
    iron_exp_list = iron_exp_f.read().splitlines()
with open(os.path.relpath('new_cdf\\elec_made_cdf.txt'), 'r') as elec_exp_f, \
    open(os.path.relpath('new_cdf\\motor_made_cdf.txt'), 'r') as motor_exp_f:
    elec_exp_list = elec_exp_f.read().splitlines()
    motor_exp_list = motor_exp_f.read().splitlines()
distList = {'motor': motor_exp_list, 'elec': elec_exp_list, 'pvc': pvc_exp_list, 'iron': iron_exp_list}
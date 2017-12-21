import math
import ctypes as ct
from config_c import *

def epanet(batch, simType, dbCursor, dbObject):
    epaCount = 0
    biHour = (batch * 4380)
    time.contents = ct.c_long(0)

    while epaCount < 4380:
        dayCount = math.floor(biHour / 12)
        tasMaxACT = float(tasMaxACTList[simType][dayCount])
        normal_run = 1

        for comp in data[simType]:
            for index, item in enumerate(data[simType][comp]['index']):
                # If the pipe is already in the failed stae
                if (int(data[simType][comp]['fS'][index]) != 0):
                    data[simType][comp]['fS'][index] = int(data[simType][comp]['fS'][index]) - 1
                    if (int(data[simType][comp]['fS'][index]) <= 0):
                        # pipe enable
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(1.0))
                        # no-time simulation config stuff
                        if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
                            reset_exposure(simType, comp, index)
                    # Pipe disable mid run
                    else:
                        normal_run = 0
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(0.0))
                        
                if ((simType == 'noTime') or (int(data[simType][comp]['fS'][index]) == 0)):
                    failure_det = failure_evaluation(comp, simType, index, tasMaxACT)
                    if (failure_det == True):
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(0.0))
                        with open(('{}_{}_fail.txt').format(simType, comp), 'a') as failure_f:
                            failure_f.write('%s %s\n' % (index, biHour))
                        dbCursor.execute('''INSERT INTO failureData VALUES (?, ?, ?)''', (biHour, index, comp))
                        if (comp != 'pump'):
                            data[simType][comp]['fS'][index] = 44
                        else:
                            data[simType][comp]['fS'][index] = 8
                        # This is based off of the 88 hr repair time, can be
                        # changed to w/e
       # Does the hydraulic solving
        if (normal_run == 0):
            epalib.ENrunH(time)
            intCount = 1
            while (intCount < nodeCount.contents.value):
                epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
                epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
                dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', \
                    (biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value))
                intCount += 1
        else:
            if (len(normal_run_list[int(biHour % 24)]) == 0):
                epalib.ENrunH(time)
                intCount = 1
                while (intCount < nodeCount.contents.value):
                    epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
                    epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
                    dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', \
                        (biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value))
                    normal_run_list[int(biHour % 24)].append([(nodeID.value).decode('utf-8'), nodeValue.contents.value])
                    intCount += 1
            else:
                for item in normal_run_list[int(biHour % 24)]:
                    dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', (biHour, item[0], item[1]))
        if (time.contents.value == 86400):
            time.contents = ct.c_int(0)
        epalib.ENnextH(timestep)

        # Saves the hydraulic results file
        # epalib.ENsaveH()
        # Reports the data from the previous run
        # epalib.ENreport()
        # epalib.ENclose()

        # Closes all of the files open during the simulation
        biHour += 1
        epaCount += 1
    dbObject.commit()

def failure_evaluation(comp, simType, index, tasMaxACT):
    if (comp != 'pump'):
        exp_from_dict = [data[simType][comp]['exp']]
        ltH_from_dict = [data[simType][comp]['ltH']]
        ctH_from_dict = [data[simType][comp]['ctH']]
        failure_dist = [comp]
    else:
        exp_from_dict = [data[simType][comp]['motor_exp'], data[simType][comp]['elec_exp']]
        ltH_from_dict = [data[simType][comp]['motor_ltH'], data[simType][comp]['elec_ltH']]
        ctH_from_dict = [data[simType][comp]['motor_ctH'], data[simType][comp]['elec_ctH']]
        failure_dist = ['motor', 'elec']
    failure_flag = False
    for fail_type, exp_list in enumerate(exp_from_dict):
        per_failed1 = distList[failure_dist[fail_type]][math.floor(float(exp_list[index]))]
        per_failed2 = distList[failure_dist[fail_type]][math.ceil(float(exp_list[index]))]
        per_failed = (float(per_failed2) - float(per_failed1)) * (float(exp_list[index]) - math.floor(float(exp_list[index]))) + float(per_failed1)
        if (per_failed > float(ctH_from_dict[fail_type][index])):
            if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
                exp_list[index] = 0
                # data[simType][comp]['tH'][index] = (np.random.uniform(0, 1, 1)[0])
                indexOfctH = (ltH_from_dict[fail_type][index].index(ctH_from_dict[fail_type][index])) + 1
                ctH_from_dict[fail_type][index] = ltH_from_dict[fail_type][index][indexOfctH]
            failure_flag = True
            return failure_flag
    if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
        exp_list[index] = float(exp_list[index]) + (biHourToYear * tasMaxACT)

    return failure_flag


def reset_exposure(simType, comp, index):
    if (comp != 'pump'):
        exp_from_dict = [data[simType][comp]['exp']]
    else:
        exp_from_dict = [data[simType][comp]['motor_exp'], data[simType][comp]['elec_exp']]

    for fail_type, exp_list in enumerate(exp_from_dict):
        exp_list[index] = 0
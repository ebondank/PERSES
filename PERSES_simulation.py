import math
import ctypes as ct
from PERSES_configuration import *

def EPANET_simulation(batch, simType):
    epaCount = 0
    biHour = (batch * 4380)
    time.contents = ct.c_long(0)
    node_data = list()
    failure_data = list()
    # Currently set to do year long batches
    while epaCount < 4380:
        dayCount = math.floor(biHour / 12)
        # Temperature at Surface maximum at current timestep
        tasMaxACT = float(tasMaxACTList[simType][dayCount])
        # Normal run used to track state of EPANET simulation
        normal_run = 1
        # Comp = Component, iterates over all component types in the simulation
        for comp in data[simType]:
            # Iterates over all instances of each component type, eg. PVC_1, PVC_2, etc, for all PVC
            for index, item in enumerate(data[simType][comp]['index']):
                # If the pipe is already in the failed stae
                if data[simType][comp]['fS'][index] != 0:
                    data[simType][comp]['fS'][index] = int(data[simType][comp]['fS'][index]) - 1
                    if (int(data[simType][comp]['fS'][index]) <= 0):
                        # Turning the pipe back on in the simulation
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(1.0))
                        # no-time simulation config stuff
                        if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
                            reset_exposure(simType, comp, index)
                    else:
                        # Pipe disable mid run
                        normal_run = 0
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(0.0))
                # noTime has a special set of configurations, just ignore
                # Testing if component is not failed, can't fail already failed component
                if (simType == 'noTime' or data[simType][comp]['fS'][index]) == 0:
                    # Failure determination module, can be modified for individual uses
                    failure_det = failure_evaluation(comp, simType, index, tasMaxACT)
                    # If the component should be failed, we turn it off and record the failure in both locations
                    if (failure_det == True):
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(0.0))
                        # with open(('{}_{}_fail.txt').format(simType, comp), 'a') as failure_f:
                            # failure_f.write('%s %s\n' % (index, biHour))
                        failure_data.append(tuple([biHour, index, comp]))
                        # dbCursor.execute('''INSERT INTO failureData VALUES (?, ?, ?)''', (biHour, index, comp))
                        # It is now an abnormal run, and we set the failure state of the component according to given values
                        normal_run = 0
                        if (comp != 'pump'):
                            data[simType][comp]['fS'][index] = 44
                        else:
                            data[simType][comp]['fS'][index] = 8
       # Does the hydraulic solving via EPANET, saves the results in our DB
        if (normal_run == 0):
            epalib.ENrunH(time)
            intCount = 1
            while (intCount < nodeCount.contents.value):
                epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
                epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
                # dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', \
                    # (biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value))
                node_data.append(tuple([biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value]))
                intCount += 1
        else:
            if (len(normal_run_list[int(biHour % 24)]) == 0):
                epalib.ENrunH(time)
                intCount = 1
                while (intCount < nodeCount.contents.value):
                    epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
                    epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
                    # dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', \
                        # (biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value))
                    node_data.append(tuple([biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value]))
                    normal_run_list[int(biHour % 24)].append([(nodeID.value).decode('utf-8'), nodeValue.contents.value])
                    intCount += 1
            else:
                for item in normal_run_list[int(biHour % 24)]:
                    # dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', (biHour, item[0], item[1]))
                    node_data.append(tuple([biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value]))
        if (time.contents.value == 86400):
            time.contents = ct.c_int(0)
        epalib.ENnextH(timestep)
        biHour += 1
        epaCount += 1
    return {"failure_data": failure_data, "node_data": node_data}
    # dbObject.commit()

def failure_evaluation(comp, simType, index, tasMaxACT):
    # Pumps have multiple failure mechanisms (electrical and motor), so they have special treatment
    # Everything treated as "lists" for code reusability
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
    # Use failure flag to signal to w/e called this function
    failure_flag = False
    for fail_type, exp_list in enumerate(exp_from_dict):
        # Exposure calculations used for failure determination
        per_failed1 = distList[failure_dist[fail_type]][math.floor(float(exp_list[index]))]
        per_failed2 = distList[failure_dist[fail_type]][math.ceil(float(exp_list[index]))]
        per_failed = (float(per_failed2) - float(per_failed1)) * (float(exp_list[index]) - math.floor(float(exp_list[index]))) + float(per_failed1)
        # If component failed, again ignore simType testing, very specific use-case
        if (per_failed > float(ctH_from_dict[fail_type][index])):
            if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
                exp_list[index] = 0
                indexOfctH = (ltH_from_dict[fail_type][index].index(ctH_from_dict[fail_type][index])) + 1
                ctH_from_dict[fail_type][index] = ltH_from_dict[fail_type][index][indexOfctH]
            failure_flag = True
            return failure_flag
    if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
        exp_list[index] = float(exp_list[index]) + (biHourToYear * tasMaxACT)

    return failure_flag


def reset_exposure(simType, comp, index):
    # Used for resetting exposure, again using lists due to pump failure mechanism
    if (comp != 'pump'):
        exp_from_dict = [data[simType][comp]['exp']]
    else:
        exp_from_dict = [data[simType][comp]['motor_exp'], data[simType][comp]['elec_exp']]

    for fail_type, exp_list in enumerate(exp_from_dict):
        exp_list[index] = 0
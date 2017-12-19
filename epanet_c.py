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

        ############### PVC PIPE ##### PVC PIPE ##### PVC PIPE ####################
        for comp in data[simType]:
            for index, item in enumerate(data[simType][comp]['index']):
                # If the pipe is already in the failed stae
                if (int(data[simType][comp]['fS'][index]) == 0):
                    data[simType][comp]['fS'][index] = int(data[simType][comp]['fS'][index]) - 1
                    if (int(data[simType][comp]['fS'][index]) <= 0):
                        # pipe enable
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(1.0))
                        # no-time simulation config stuff
                        if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
                            data[simType][comp]['exp'][index] = 0
                    # Pipe disable mid run
                    else:
                        normal_run = 0
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(0.0))
                        
                if ((simType == 'noTime') or (int(data[simType][comp]['fS'][index]) == 0)):
                    per_failed1 = distList[comp][math.floor(float(data[simType][comp]['exp'][index]))]
                    per_failed2 = distList[comp][math.ceil(float(data[simType][comp]['exp'][index]))]
                    per_failed = (float(per_failed2) - float(per_failed1)) * (float(data[simType][comp]['exp'][index]) - math.floor(float(data[simType][comp]['exp'][index]))) + float(per_failed1)
                    if (per_failed > float(data[simType][comp]['ctH'][index])):
                        if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
                            data[simType][comp]['exp'][index] = 0
                            # data[simType][comp]['tH'][index] = (np.random.uniform(0, 1, 1)[0])
                            indexOfctH = data[simType][comp]['ltH'][index].index(data[simType][comp]['ctH'][index]) + 1
                            data[simType][comp]['ctH'][index] = data[simType][comp]['ltH'][index][indexOfctH]

                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(0.0))
                        pipeFailureFile = open(('{}_pvcPipeFail.txt').format(simType), 'a')
                        pipeFailureFile.write('%s %s\n' % (index, biHour))
                        pipeFailureFile.close()
                        dbCursor.execute('''INSERT INTO failureData VALUES (?, ?, ?)''', (biHour, index, comp))
                        data[simType][comp]['fS'][index] = 44
                        # This is based off of the 88 hr repair time, can be
                        # changed to w/e
                    if ((simType == 'noTemp') or (simType == 'real') or (simType == 'historical')):
                        data[simType][comp]['exp'][index] = float(data[simType][comp]['exp'][index]) \
                            + (biHourToYear * tasMaxACT)
                    if (data[simType][comp]['fS'][index] == 0):
                        epalib.ENsetlinkvalue(data[simType][comp]['index'][index], ct.c_int(11), ct.c_float(1.0))

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
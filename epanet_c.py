import math
import ctypes as ct
from config_c import *


def epanet(batch, simType, dbCursor, dbObject):
    epaCount = 0
    biHour = (batch * 8760)
    
    time.contents = ct.c_long(0)

    while epaCount < 8760:
        dayCount = math.floor(biHour / 24)
        tasMaxACT = float(tasMaxACTList[simType][dayCount])
        normal_run = 1
        ############### PVC PIPE ##### PVC PIPE ##### PVC PIPE ####################
        for index, item in enumerate(data[simType]['pvc']['index']):
            # If the pipe is already in the failed state
            if (int(data[simType]['pvc']['fS'][index]) != 0):
                data[simType]['pvc']['fS'][index] = int(data[simType]['pvc']['fS'][index]) - 1
                if (int(data[simType]['pvc']['fS'][index]) <= 0):
                    # pipe enable
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(1.0))
                    # no-time simulation config stuff
                    if ((simType == 'noTemp') or (simType == 'real')):
                        data[simType]['pvc']['age'][index] = biHourToYear
                # Pipe disable mid run
                else:
                    normal_run = 0
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(0.0))
                    
            elif ((simType == 'noTime') or (int(data[simType]['pvc']['fS'][index]) == 0)):
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 20)
                if indexSelect <= 0:
                    indexSelect = 0
                indexSelect = indexSelect + int(30 * int(math.trunc(float(data[simType]['pvc']['age'][index]))))
                weibullApprox = float(pvcWeibullList[indexSelect])
                tempDecimal = (((tasMaxACT - math.trunc(tasMaxACT)) / tasMaxACT) * float(pvcWeibullList[indexSelect]))
                ageDecimal = (((data[simType]['pvc']['age'][index] - math.trunc(data[simType]['pvc']['age'][index])) / data[simType]['pvc']['age'][index]) * float(pvcWeibullList[indexSelect]))
                weibullApprox = weibullApprox + tempDecimal + ageDecimal
                if (weibullApprox > float(data[simType]['pvc']['ctH'][index])):
                    normal_run = 0
                    if ((simType == 'noTemp') or (simType == 'real')):
                        data[simType]['pvc']['age'][index] = biHourToYear
                        # data[simType]['pvc']['tH'][index] = (np.random.uniform(0, 1, 1)[0])
                        indexOfctH = data[simType]['pvc']['ltH'][index].index(data[simType]['pvc']['ctH'][index]) + 1
                        data[simType]['pvc']['ctH'][index] = data[simType]['pvc']['ltH'][index][indexOfctH]

                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(0.0))
                    pipeFailureFile = open(('{}_pvcPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    dbCursor.execute('''INSERT INTO failureData VALUES (?, ?, ?)''', (biHour, index, 'pvc'))
                    data[simType]['pvc']['fS'][index] = 44
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                if ((simType == 'noTemp') or (simType == 'real')):
                    data[simType]['pvc']['age'][index] = float(data[simType]['pvc']['age'][index]) + biHourToYear

                if (data[simType]['pvc']['fS'][index] == 0):
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(1.0))


        #################### IRON PIPE ##### IRON PIPE ##### IRON PIPE ####################
        for index, item in enumerate(data[simType]['iron']['index']):
            # Handling failed components
            if (int(data[simType]['iron']['fS'][index]) != 0):
                data[simType]['iron']['fS'][index] = int(data[simType]['iron']['fS'][index]) - 1
                if (int(data[simType]['iron']['fS'][index]) <= 0):
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(1.0))

                else:
                    normal_run = 0
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(0.0))

                if (simType == ('noTemp' or 'real')):
                    data[simType]['iron']['age'][index] = biHourToYear

            # Currently functional and testing for failure
            elif (simType == 'noTime') or (int(data[simType]['iron']['fS'][index]) == 0):
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 20)
                if indexSelect < 0:
                    indexSelect = 0

                indexSelect = indexSelect + (30 * int(math.trunc(float(data[simType]['iron']['age'][index]))))
                weibullApprox = float(ironWeibullList[indexSelect])
                tempDecimal = (((tasMaxACT - math.trunc(tasMaxACT)) / tasMaxACT) * float(ironWeibullList[indexSelect]))
                ageDecimal = (((data[simType]['iron']['age'][index] - math.trunc(data[simType]['iron']['age'][index])) / data[simType]['iron']['age'][index]) * float(ironWeibullList[indexSelect]))
                weibullApprox = weibullApprox + tempDecimal + ageDecimal
                if (weibullApprox > float(data[simType]['iron']['ctH'][index])):
                    normal_run = 0
                    if ((simType == 'noTemp') or (simType == 'real')):
                        data[simType]['iron']['age'][index] = biHourToYear
                        # data[simType]['iron']['tH'][index] = (np.random.uniform(0, 1, 1)[0])
                        indexOfctH = data[simType]['iron']['ltH'][index].index(data[simType]['iron']['ctH'][index]) + 1
                        data[simType]['iron']['ctH'][index] = data[simType]['iron']['ltH'][index][indexOfctH]

                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(0.0))
                    # Writing to the seperate failure statistics file
                    pipeFailureFile = open(('{}_ironPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    dbCursor.execute('''INSERT INTO failureData VALUES (?, ?, ?)''', (biHour, index, 'iron'))
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    data[simType]['iron']['fS'][index] = 44
                if ((simType == 'noTemp') or (simType == 'real')):
                    data[simType]['iron']['age'][index] = float(data[simType]['iron']['age'][index]) + biHourToYear

                if (data[simType]['iron']['fS'][index] == 0):
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(1.0))

        ######################### PUMPS ##### PUMPS ##### PUMPS #############################################
        for index, item in enumerate(data[simType]['pump']['index']):
            # If component in failed state
            if (data[simType]['pump']['fS'][index] != 0):
                data[simType]['pump']['fS'][index] = int(data[simType]['pump']['fS'][index]) - 1

                if (int(data[simType]['pump']['fS'][index]) <= 0):
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(11), ct.c_float(1.0))
                    if ((simType == 'noTemp') or (simType == 'real')):
                        data[simType]['pump']['age'][index] = biHourToYear
                else:
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(11), ct.c_float(0.0))
                    normal_run = 0

            # Not currently failed block
            elif ((simType == "noTime") or (data[simType]['pump']['fS'][index] == 0)):
                indexSelect = (math.trunc(tasMaxACT) - 20)
                if indexSelect < 0:
                    indexSelect = 0

                indexSelect = indexSelect + (30 * int(math.trunc(float(data[simType]['pump']['age'][index]))))
                tempDecimal = (((tasMaxACT - math.trunc(tasMaxACT)) / tasMaxACT) * float(pumpWeibullList[indexSelect]))
                ageDecimal = (((data[simType]['pump']['age'][index] - math.trunc(data[simType]['pump']['age'][index])) / data[simType]['pump']['age'][index]) * float(pumpWeibullList[indexSelect]))
                weibullApprox = float(pumpWeibullList[indexSelect]) + tempDecimal + ageDecimal
                if (weibullApprox > float(data[simType]['pump']['ctH'][index])):
                    normal_run = 0
                    if ((simType == 'noTemp') or (simType == 'real')):
                        data[simType]['pump']['age'][index] = 0
                        # data[simType]['pump']['tH'][index] = (np.random.uniform(0, 1, 1)[0])
                        indexOfctH = data[simType]['pump']['ltH'][index].index(data[simType]['pump']['ctH'][index]) + 1
                        data[simType]['pump']['ctH'][index] = data[simType]['pump']['ltH'][index][indexOfctH]

                    pumpFailureFile = open(('{}_pumpFail.txt').format(simType), 'a')
                    pumpFailureFile.write('%s %s\n' % (index, biHour))
                    pumpFailureFile.close()
                    dbCursor.execute('''INSERT INTO failureData VALUES (?, ?, ?)''', (biHour, index, 'pump'))
                    
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(11), ct.c_float(0.0))
                    # This is based off of the 16 hr repair time, can be
                    # changed to w/e
                    data[simType]['pump']['fS'][index] = 8
                if ((simType == 'noTemp') or (simType == 'real')):
                    data[simType]['pump']['age'][index] = float(data[simType]['pump']['age'][index]) + biHourToYear
                if (data[simType]['pump']['fS'][index] == 0):
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(11), ct.c_float(1.0))

        # Does the hydraulic solving
        # print('errorcode: %s' % errorcode)
        if (normal_run == 0):
            epalib.ENrunH(time)
            intCount = 1
            while (intCount < nodeCount.contents.value):
                epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
                epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
                dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', (biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value))
                # print(('{} {} {} \n').format(biHour, nodeID.value, nodeValue.contents.value))
                intCount += 1
        else:
            if (len(normal_run_list[int(biHour % 24)]) == 0):
                epalib.ENrunH(time)
                intCount = 1
                while (intCount < nodeCount.contents.value):
                    epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
                    epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
                    dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', (biHour, (nodeID.value).decode('utf-8'), nodeValue.contents.value))
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
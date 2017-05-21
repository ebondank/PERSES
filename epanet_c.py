import math
import numpy as np
import ctypes as ct
from config_c import *


def epanet(batch, simType, dbCursor, dbObject):
    epaCount = 0
    biHour = (batch * 8760)
    # Makes sure time == 0 (start of new 'batch')
    # Also sets all of the components to functional, will eliminate 1/8760 edge case
    # Those that are properly failed will go back into the failed state
    time.contents = ct.c_int(0)
    for index, item in enumerate(data[simType]['pvc']['fS']):
        epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(1))
    for index, item in enumerate(data[simType]['iron']['fS']):
        epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(1))
    for index, item in enumerate(data[simType]['pump']['fS']):
        epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(12), ct.c_float(1))
    while epaCount < 5:
        dayCount = math.floor(biHour / 24)
        tasMaxACT = float(tasMaxACTList[simType][dayCount])

        for index, item in enumerate(data[simType]['pvc']['index']):
            # If the pipe is already in the failed state
            if (int(data[simType]['pvc']['fS'][index]) != 0):
                data[simType]['pvc']['fS'][index] = data[simType]['pvc']['fS'][index] - 1

                if (int(data[simType]['pvc']['fS'][index]) <= 0):
                    # pipe enable
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(1))
                    # no-time simulation config stuff
                    if (simType != 'noTime'):
                        data[simType]['pvc']['age'][index] = 0
                # Pipe disable mid run
                else:
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(0.0))
            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect <= 0:
                    indexSelect = 0
                indexSelect = indexSelect + int(30 * int(math.trunc(float(data[simType]['pvc']['age'][index]))))

                if (float(pvcWeibullList[indexSelect]) > float(data[simType]['pvc']['tH'][index])):
                    data[simType]['pvc']['age'][index] = 0
                    data[simType]['pvc']['tH'][index] = float((np.random.uniform(0, 1, 1))[0])
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index], ct.c_int(11), ct.c_float(0.0))
                    pipeFailureFile = open(('{}_pvcPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    data[simType]['pvc']['fS'][index] = 44
                if (simType != 'noTime'):
                    data[simType]['pvc']['age'][index] = float(data[simType]['pvc']['age'][index]) + biHourToYear

        for index, item in enumerate(data[simType]['iron']['index']):
            if (int(data[simType]['iron']['fS'][index]) != 0):
                data[simType]['iron']['fS'][index] = int(data[simType]['iron']['fS'][index]) - 1
                if (int(data[simType]['iron']['fS'][index]) <= 0):
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(1))
                else:
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(0.0))
                if (simType != 'noTime'):
                    data[simType]['iron']['age'][index] = 0

            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + (30 * int(math.trunc(float(data[simType]['iron']['age'][index]))))

                if (float(ironWeibullList[indexSelect]) > float(data[simType]['iron']['tH'][index])):
                    if (simType != 'noTime'):
                        data[simType]['iron']['age'][index] = 0
                    data[simType]['iron']['tH'][index] = float((np.random.uniform(0, 1, 1))[0])
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index], ct.c_int(11), ct.c_float(0.0))
                    # Writing to the seperate failure statistics file
                    pipeFailureFile = open(('{}_ironPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    data[simType]['iron']['fS'][index] = 44
                if (simType != 'noTime'):
                    data[simType]['iron']['age'][index] = float(data[simType]['iron']['age'][index]) + biHourToYear
        for index, item in enumerate(data[simType]['pump']['index']):
            data[simType]['pump']['fS'][index] = -1
            if (data[simType]['pump']['fS'][index] != 0):
                data[simType]['pump']['fS'][index] = int(data[simType]['pump']['fS'][index]) - 1
                epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(12), ct.c_float(0.0))
                if (int(data[simType]['pump']['fS'][index]) <= 0):
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(12), ct.c_float(1.0))
                    if (simType != 'noTime'):
                        data[simType]['pump']['age'][index] = 0

            else:
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + (30 * int(math.trunc(float(data[simType]['pump']['age'][index]))))
                if float(pumpWeibullList[indexSelect]) > float(data[simType]['pump']['tH'][index]):
                    if (simType != 'noTime'):
                        data[simType]['pump']['age'][index] = 0
                    data[simType]['pump']['tH'][index] = float((np.random.uniform(0, 1, 1))[0])
                    pumpFailureFile = open(('{}_pumpFail.txt').format(simType), 'a')
                    pumpFailureFile.write('%s %s\n' % (index, biHour))
                    pumpFailureFile.close()
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index], ct.c_int(12), ct.c_float(0.0))
                    # This is based off of the 16 hr repair time, can be
                    # changed to w/e
                    data[simType]['pump']['fS'][index] = 8
                if (simType != 'noTime'):
                    data[simType]['pump']['age'][index] = float(data[simType]['pump']['age'][index]) + biHourToYear

        # Does the hydraulic solving
        # print('errorcode: %s' % errorcode)
        epalib.ENrunH(time)
        intCount = ct.c_int(1)
        while (intCount.value < nodeCount.contents.value):
            epalib.ENgetnodevalue(intCount, ct.c_int(11), nodeValue)
            epalib.ENgetnodeid(intCount, nodeID)
            dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', (biHour, nodeID.value, nodeValue.contents.value))
            # print(('{} {} {} \n').format(biHour, nodeID.value, nodeValue.contents.value))
            intCount.value = intCount.value + 1

        dbObject.commit()
        if (time.contents.value == 864000):
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

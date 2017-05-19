import math
from config_c import *
import numpy as np
import ctypes as ct
import parent_c


def epanet(batch, simType, dbCursor, dbObject):
    epaCount = 0
    biHour = (batch * 144)
    while epaCount < 144:
        dayCount = math.floor(biHour / 12)
        tasMaxACT = float(tasMaxACTList[simType][dayCount])

        for index, item in enumerate(data[simType]['pvc']):
            # If the pipe is already in the failed state
            if (int(data[simType]['pvc']['fS'][index + 1]) != 0):
                data[simType]['pvc']['fS'][index + 1] = data[simType]['pvc']['fS'][index + 1] - 1

                if (int(data[simType]['pvc']['fS'][index + 1]) <= 0):
                    # pipe enable
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index + 1], ct.c_int(11), ct.c_float(1))
                    # no-time simulation config stuff
                    if (simType != 'noTime'):
                        pvcPipeAges[simType][index + 1] = 0
                # Pipe disable mid run
                else:
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect <= 0:
                    indexSelect = 0
                indexSelect += 30 * int(math.trunc(float(data[simType]['pvc']['age'][index + 1])))

                if (float(pvcWeibullList[index + 1Select]) > float(data[simType]['pvc']['tH'][index + 1])):
                    data[simType]['pvc']['age'][index + 1] = 0
                    data[simType]['pvc']['tH'][index + 1] = float((np.random.uniform(0, 1, 1))[0])
                    epalib.ENsetlinkvalue(data[simType]['pvc']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
                    pipeFailureFile = open(('{}_pvcPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    data[simType]['pvc']['fS'][index + 1] = 44
                if (simType != 'noTime'):
                    data[simType]['pvc']['age'][index + 1] = float(data[simType]['pvc']['age'][index + 1]) + biHourToYear

        for index, item in enumerate(ironPipesList):
            if (int(data[simType]['iron']['fS'][index + 1]) != 0):
                data[simType]['iron']['fS'][index + 1] = int(data[simType]['iron']['fS'][index + 1]) - 1
                if (int(data[simType]['iron']['fS'][index + 1]) <= 0):
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index + 1], ct.c_int(11), ct.c_float(1))
                else:
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
                if (simType != 'noTime'):
                    data[simType]['iron']['age'][index + 1] = 0

            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + (30 * int(math.trunc(float(data[simType]['iron']['age'][index + 1]))))

                if (float(ironWeibullList[index + 1Select]) > float(data[simType]['iron']['tH'][index + 1])):
                    if (simType != 'noTime'):
                        data[simType]['iron']['age'][index + 1] = 0
                    data[simType]['iron']['tH'][index + 1] = float((np.random.uniform(0, 1, 1))[0])
                    epalib.ENsetlinkvalue(data[simType]['iron']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
                    # Writing to the seperate failure statistics file
                    pipeFailureFile = open(('{}_ironPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    data[simType]['iron']['fS'][index + 1] = 44
                if (simType != 'noTime'):
                    data[simType]['iron']['age'][index + 1] = float(data[simType]['iron']['age'][index + 1]) + biHourToYear
        for index, item in enumerate(pumpList):
            if (int(data[simType]['pump']['fS'][index + 1]) != 0):
                data[simType]['pump']['fS'][index + 1] = int(data[simType]['pump']['fS'][index + 1]) - 1
                epalib.ENsetlinkvalue(data[simType]['pump']['index'][index + 1], ct.c_int(12), ct.c_float(0.0))
                if (int(data[simType]['pump']['fS'][index + 1]) <= 0):
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index + 1], ct.c_int(12), ct.c_float(1.0))
                    if (simType != 'noTime'):
                        data[simType]['pump']['age'][index + 1] = 0

            else:
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + (30 * int(math.trunc(float(data[simType]['pump']['age'][index + 1]))))
                if float(pumpWeibullList[index + 1Select]) > float(data[simType]['pump']['tH'][index + 1]):
                    if (simType != 'noTime'):
                        data[simType]['pump']['age'][index + 1] = 0
                    data[simType]['pump']['tH'][index + 1] = float((np.random.uniform(0, 1, 1))[0])
                    pumpFailureFile = open(('{}_pumpFail.txt').format(simType), 'a')
                    pumpFailureFile.write('%s %s\n' % (index, biHour))
                    pumpFailureFile.close()
                    epalib.ENsetlinkvalue(data[simType]['pump']['index'][index + 1], ct.c_int(12), ct.c_float(0.0))
                    # This is based off of the 16 hr repair time, can be
                    # changed to w/e
                    pumpFailureStatus[simType][index + 1] = 8
                if (simType != 'noTime'):
                    data[simType]['pump']['age'][index + 1] = float(data[simType]['pump']['age'][index + 1]) + biHourToYear

        # Does the hydraulic solving
        errorcode = parent_c.epalib.ENrunH(time)
        print('errorcode: %s' % errorcode)

        intCount = ct.c_int(1)
        while (intCount.value < nodeCount.contents.value):
            parent_c.epalib.ENgetnodevalue(intCount, ct.c_int(11), nodeValue)
            parent_c.epalib.ENgetnodeid(intCount, nodeID)
            dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', (biHour, nodeID.value, nodeValue.contents.value))
            intCount.value = intCount.value + 1

        dbObject.commit()
        if (parent_c.time.contents.value == 864000):
            parent_c.time.contents = ct.c_int(0)
        parent_c.epalib.ENnextH(parent_c.timestep)

        # Saves the hydraulic results file
        # epalib.ENsaveH()
        # Reports the data from the previous run
        # epalib.ENreport()
        # epalib.ENclose()

        # Closes all of the files open during the simulation
        f.close()
        fi.close()
        biHour += 1
        epaCount += 1

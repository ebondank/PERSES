import math
import numpy as np
import ctypes as ct
import parent_c
import config_c


def epanet(batch, simType, dbCursor, dbObject):
    epaCount = 0
    config_c.biHour = (batch * 144)
    while epaCount < 144:
        dayCount = math.floor(config_c.biHour / 12)
        tasMaxACT = float(parent_c.tasMaxACTList[simType][dayCount])

        for index, item in enumerate(config_c.data[simType]['pvc']['index']):
            # If the pipe is already in the failed state
            if (int(config_c.data[simType]['pvc']['fS'][index + 1]) != 0):
                config_c.data[simType]['pvc']['fS'][index + 1] = config_c.data[simType]['pvc']['fS'][index + 1] - 1

                if (int(config_c.data[simType]['pvc']['fS'][index + 1]) <= 0):
                    # pipe enable
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['pvc']['index'][index + 1], ct.c_int(11), ct.c_float(1))
                    # no-time simulation config stuff
                    if (simType != 'noTime'):
                        config_c.data[simType]['pvc']['age'] = 0
                # Pipe disable mid run
                else:
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['pvc']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect <= 0:
                    indexSelect = 0
                indexSelect += 30 * int(math.trunc(float(config_c.data[simType]['pvc']['age'][index + 1])))

                if (float(config_c.pvcWeibullList[indexSelect]) > float(config_c.data[simType]['pvc']['tH'][index + 1])):
                    config_c.data[simType]['pvc']['age'][index + 1] = 0
                    config_c.data[simType]['pvc']['tH'][index + 1] = float((np.random.uniform(0, 1, 1))[0])
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['pvc']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
                    pipeFailureFile = open(('{}_pvcPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, config_c.biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    config_c.data[simType]['pvc']['fS'][index + 1] = 44
                if (simType != 'noTime'):
                    config_c.data[simType]['pvc']['age'][index + 1] = float(config_c.data[simType]['pvc']['age'][index + 1]) + config_c.biHourToYear

        for index, item in enumerate(config_c.data[simType]['iron']['index']):
            if (int(config_c.data[simType]['iron']['fS'][index + 1]) != 0):
                config_c.data[simType]['iron']['fS'][index + 1] = int(config_c.data[simType]['iron']['fS'][index + 1]) - 1
                if (int(config_c.data[simType]['iron']['fS'][index + 1]) <= 0):
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['iron']['index'][index + 1], ct.c_int(11), ct.c_float(1))
                else:
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['iron']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
                if (simType != 'noTime'):
                    config_c.data[simType]['iron']['age'][index + 1] = 0

            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + (30 * int(math.trunc(float(config_c.data[simType]['iron']['age'][index + 1]))))

                if (float(config_c.ironWeibullList[indexSelect]) > float(config_c.data[simType]['iron']['tH'][index + 1])):
                    if (simType != 'noTime'):
                        config_c.data[simType]['iron']['age'][index + 1] = 0
                    config_c.data[simType]['iron']['tH'][index + 1] = float((np.random.uniform(0, 1, 1))[0])
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['iron']['index'][index + 1], ct.c_int(11), ct.c_float(0.0))
                    # Writing to the seperate failure statistics file
                    pipeFailureFile = open(('{}_ironPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, config_c.biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    config_c.data[simType]['iron']['fS'][index + 1] = 44
                if (simType != 'noTime'):
                    config_c.data[simType]['iron']['age'][index + 1] = float(config_c.data[simType]['iron']['age'][index + 1]) + config_c.biHourToYear
        for index, item in enumerate(config_c.data[simType]['pump']['id']):
            if (int(config_c.data[simType]['pump']['fS'][index + 1]) != 0):
                config_c.data[simType]['pump']['fS'][index + 1] = int(config_c.data[simType]['pump']['fS'][index + 1]) - 1
                parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['pump']['index'][index + 1], ct.c_int(12), ct.c_float(0.0))
                if (int(config_c.data[simType]['pump']['fS'][index + 1]) <= 0):
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['pump']['index'][index + 1], ct.c_int(12), ct.c_float(1.0))
                    if (simType != 'noTime'):
                        config_c.data[simType]['pump']['age'][index + 1] = 0

            else:
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + (30 * int(math.trunc(float(config_c.data[simType]['pump']['age'][index + 1]))))
                if float(config_c.pumpWeibullList[indexSelect]) > float(config_c.data[simType]['pump']['tH'][index + 1]):
                    if (simType != 'noTime'):
                        config_c.data[simType]['pump']['age'][index + 1] = 0
                    config_c.data[simType]['pump']['tH'][index + 1] = float((np.random.uniform(0, 1, 1))[0])
                    pumpFailureFile = open(('{}_pumpFail.txt').format(simType), 'a')
                    pumpFailureFile.write('%s %s\n' % (index, config_c.biHour))
                    pumpFailureFile.close()
                    parent_c.epalib.ENsetlinkvalue(config_c.data[simType]['pump']['index'][index + 1], ct.c_int(12), ct.c_float(0.0))
                    # This is based off of the 16 hr repair time, can be
                    # changed to w/e
                    config_c.data[simType]['pump']['fS'][index + 1] = 8
                if (simType != 'noTime'):
                    config_c.data[simType]['pump']['age'][index + 1] = float(config_c.data[simType]['pump']['age'][index + 1]) + config_c.biHourToYear

        # Does the hydraulic solving
        errorcode = parent_c.epalib.ENrunH(parent_c.time)
        print('errorcode: %s' % errorcode)

        intCount = ct.c_int(1)
        while (parent_c.intCount.value < parent_c.nodeCount.contents.value):
            parent_c.epalib.ENgetnodevalue(parent_c.intCount, ct.c_int(11), parent_c.nodeValue)
            parent_c.epalib.ENgetnodeid(parent_c.intCount, parent_c.nodeID)
            dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', (config_c.biHour, parent_c.nodeID.value, parent_c.nodeValue.contents.value))
            intCount.value = intCount.value + 1

        dbObject.commit()
        if (parent_c.time.contents.value == 864000):
            parent_c.time.contents = ct.c_int(0)
        parent_c.epalib.ENnextH(parent_c.timestep)

        # Saves the hydraulic results file
        # parent_c.epalib.ENsaveH()
        # Reports the config_c.data from the previous run
        # parent_c.epalib.ENreport()
        # parent_c.epalib.ENclose()

        # Closes all of the files open during the simulation
        config_c.biHour += 1
        epaCount += 1

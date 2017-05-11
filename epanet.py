from ctypes import cdll
import math
from config import *
import numpy as np
from supporting import pipeDisable, pipeFix, pumpDisable, parsingRpt


def epanet(simType, dbCursor, dbObject):
    epalib = cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')
    biHourt = 0
    while biHourt < 144:
        dayCount = math.floor(biHour / 12)
        tasMaxACT = float(tasMaxACTList[dayCount])
        periodCount = (biHour % 24)

        for index, item in enumerate(pvcPipesList):
            # If the pipe is already in the failed state
            if (int(pvcFailureStatus[index]) != 0):
                pvcFailureStatus[index] = int(pvcFailureStatus[index]) - 1
                if (int(pvcFailureStatus[index]) <= 0):
                    pipeFixCount = 0
                    while (pipeFixCount < 24):
                        pipeFix(pvcPipesList, pvcTriggerList, index, pipeFixCount)
                        pipeFixCount += 1
                    pvcPipeAges[index] = 0
                else:
                    pipeDisable(pvcPipesList, pvcTriggerList, index, periodCount)
            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect <= 0:
                    indexSelect = 0
                indexSelect += 30 * int(math.trunc(float(pvcPipeAges[index])))

                if (float(pvcWeibullList[indexSelect]) > float(pvcPipeThresholdList[index])):
                    pvcPipeAges[index] = 0
                    pvcPipeThresholdList[index] = (np.random.uniform(0, 1, 1))[0]
                    pipeDisable(pvcPipesList, pvcTriggerList, index, periodCount)
                    pipeFailureFile = open(('{}pvcPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    pvcFailureStatus[index] = 44
                config.pvcPipeAges[index] = float(config.pvcPipeAges[index]) + config.biHourToYear

        for index, item in enumerate(ironPipesList):
            if (int(ironFailureStatus[index]) != 0):
                ironFailureStatus[index] = int(ironFailureStatus[index]) - 1
                if (int(ironFailureStatus[index]) == 0):
                    ironPipeFixCount = 0
                    while (ironPipeFixCount < 24):
                        pipeFix(ironPipesList, ironTriggerList, index, ironPipeFixCount)
                        ironPipeFixCount += 1
                else:
                    pipeDisable(ironPipesList, ironTriggerList, index, periodCount)
                ironPipeAges[index] = 0

            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + (30 * int(math.trunc(float(ironPipeAges[index]))))

                if (float(ironWeibullList[indexSelect]) > float(ironPipeThresholdList[index])):
                    ironPipeAges[index] = 0
                    ironPipeThresholdList[index] = (np.random.uniform(0, 1, 1))[0]
                    pipeDisable(ironPipesList, ironTriggerList, index, periodCount)
                    # Writing to the seperate failure statistics file
                    pipeFailureFile = open(('{}ironPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    ironFailureStatus[index] = 44
                ironPipeAges[index] = float(ironPipeAges[index]) + biHourToYear
        for index, item in enumerate(pumpList):
            if (int(pumpFailureStatus[index]) != 0):
                pumpFailureStatus[index] = int(pumpFailureStatus[index]) - 1
                pumpDisable(pumpList, mutedPumpList, index, periodCount)

                if (int(pumpFailureStatus[index]) == 0):
                    pumpFixCount = 0
                    while (pumpFixCount < 24):
                        pumpDisable(mutedPumpList, pumpList,
                                    index, pumpFixCount)
                        pumpFixCount += 1
                    pumpAgeList[index] = 0

            else:
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + \
                    (30 * int(math.trunc(float(pumpAgeList[index]))))
                if float(pumpWeibullList[indexSelect]) > float(pumpThresholdList[index]):
                    pumpAgeList[index] = 0
                    pumpThresholdList[index] = (np.random.uniform(0, 1, 1))[0]
                    pumpFailureFile = open(('{}pumpFail.txt').format(simType), 'a')
                    pumpFailureFile.write('%s %s\n' % (index, biHour))
                    pumpFailureFile.close()
                    pumpDisable(pumpList, mutedPumpList, index, periodCount)
                    # This is based off of the 16 hr repair time, can be
                    # changed to w/e
                    pumpFailureStatus[index] = 8

                pumpAgeList[index] = float(pumpAgeList[index]) + biHourToYear

        f = open('D:\\Austin_Michne\\tripleSim\\input\\%s\\NorthMarin_%s.inp' % (simType, periodCount), 'r')
        fi = open('D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.rpt' % (simType, biHour), 'w')
        fu = open('D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.bin' % (simType, biHour), 'w')
        # Initializes the files for encoding
        a = 'D:\\Austin_Michne\\tripleSim\\input\\%s\\NorthMarin_%s.inp' % (simType, periodCount)
        b = 'D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.rpt' % (simType, biHour)
        c = 'D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.bin' % (simType, biHour)
        # Byte objects
        b_a = a.encode('UTF-8')
        b_b = b.encode('UTF-8')
        b_c = c.encode('UTF-8')
        # Opens the toolkit
        epalib.ENopen(b_a, b_b, b_c)
        # Does the hydraulic solving
        epalib.ENsolveH()
        # Saves the hydraulic results file
        epalib.ENsaveH()
        # Reports the data from the previous run
        epalib.ENreport()
        # Closes all of the files open during the simulation
        f.close()
        fi.close()
        fu.close()

        parsingRpt('D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.rpt' % (simType, biHour), config.databaseCursor, config.databaseObject)
        config.biHour += 1
        biHourt += 1

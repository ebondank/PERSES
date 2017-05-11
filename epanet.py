from ctypes import cdll
import math
from config import *
import numpy as np
from supporting import pipeDisable, pipeFix, pumpDisable, parsingRpt


def epanet():
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
                    pipeFailureFile = open('D:\\Austin_Michne\\1_11_18_pvcPipeFail.txt', 'a')
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
                    pipeFailureFile = open(
                        'D:\\Austin_Michne\\1_11_18_ironPipeFail.txt', 'a')
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
                    pumpFailureFile = open('D:\\Austin_Michne\\1_11_18_pumpFail.txt', 'a')
                    pumpFailureFile.write('%s %s\n' % (index, biHour))
                    pumpFailureFile.close()
                    pumpDisable(pumpList, mutedPumpList, index, periodCount)
                    # This is based off of the 16 hr repair time, can be
                    # changed to w/e
                    pumpFailureStatus[index] = 8

                pumpAgeList[index] = float(pumpAgeList[index]) + biHourToYear

        f = open('D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (periodCount), 'r')
        fi = open('D:\\Austin_Michne\\1_11_17\\output\\NorthMarin_%s.rpt' % (biHour), 'w')
        fu = open('D:\\Austin_Michne\\1_11_17\\output\\NorthMarin_%s.bin' % (biHour), 'w')
        # Initializes the files for encoding
        a = 'D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (periodCount)
        b = 'D:\\Austin_Michne\\1_11_17\\output\\NorthMarin_%s.rpt' % (biHour)
        c = 'D:\\Austin_Michne\\1_11_17\\output\\NorthMarin_%s.bin' % (biHour)
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

        parsingRpt('D:\\Austin_Michne\\1_11_17\\output\\NorthMarin_%s.rpt' % (biHour), databaseCursor, databaseObject)

        biHour += 1
        biHourt += 1

    extCountFile = open('D:\\Austin_Michne\\1_11_17\\countKeeper.txt', 'w')
    extCountFile.write('%s' % (biHour))
    extCountFile.close()

    # Iron list updating
    ironAgeFile = open('D:\\Austin_Michne\\1_11_17\\ironAgeFile.txt', 'w')
    ironFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\ironFailureStatus.txt', 'w')
    ironPipeThresholdFile = open('D:\\Austin_Michne\\1_11_17\\ironPipeThresholdFile.txt', 'w')
    for index, item in enumerate(ironPipeAges):
        ironAgeFile.write('%s\n' % ironPipeAges[index])
        ironFailureStatusFile.write('%s\n' % ironFailureStatus[index])
        ironPipeThresholdFile.write('%s\n' % ironPipeThresholdList[index])
    ironPipeThresholdFile.close()
    ironAgeFile.close()
    ironFailureStatusFile.close()

    # PVC list updating
    pvcFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\pvcFailureStatus.txt', 'w')
    pvcAgeFile = open('D:\\Austin_Michne\\1_11_17\\pvcAgeFile.txt', 'w')
    pvcPipeThresholdFile = open(
        'D:\\Austin_Michne\\1_11_17\\pvcPipeThresholdFile.txt', 'w')
    for index, item in enumerate(pvcPipeAges):
        pvcFailureStatusFile.write('%s\n' % pvcFailureStatus[index])
        pvcAgeFile.write('%s\n' % pvcPipeAges[index])
        pvcPipeThresholdFile.write('%s\n' % pvcPipeThresholdList[index])
    pvcPipeThresholdFile.close()
    pvcAgeFile.close()
    pvcFailureStatusFile.close()

    # Pump list updating
    pumpFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\pumpFailureStatus.txt', 'w')
    pumpThresholdFile = open('D:\\Austin_Michne\\1_11_17\\pumpThresholdFile.txt', 'w')
    pumpAgeFile = open('D:\\Austin_Michne\\1_11_17\\pumpAgeFile.txt', 'w')
    for index, item in enumerate(pumpAgeList):
        pumpFailureStatusFile.write('%s\n' % pumpFailureStatus[index])
        pumpThresholdFile.write('%s\n' % pumpThresholdList[index])
        pumpAgeFile.write('%s\n' % pumpAgeList[index])
    pumpAgeFile.close()
    pumpFailureStatusFile.close()
    pumpThresholdFile.close()

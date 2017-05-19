import math
from config import *
import numpy as np
from supporting import pipeDisable, pipeFix, pumpDisable, parsingRpt
import ctypes as ct


def epanet(batch, simType, dbCursor, dbObject):
    epalib = ct.cdll.LoadLibrary(
        'D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')
    epaCount = 0
    biHour = (batch * 144)
    while epaCount < 144:
        dayCount = math.floor(biHour / 12)
        tasMaxACT = float(tasMaxACTList[simType][dayCount])
        periodCount = (biHour % 24)

        for index, item in enumerate(pvcPipesList):
            # If the pipe is already in the failed state
            if (int(pvcFailureStatus[simType][index]) != 0):
                pvcFailureStatus[simType][index] = int(
                    pvcFailureStatus[simType][index]) - 1
                if (int(pvcFailureStatus[simType][index]) <= 0):
                    pipeFixCount = 0
                    while (pipeFixCount < 24):
                        pipeFix(pvcPipesList, pvcTriggerList,
                                index, pipeFixCount, simType)
                        pipeFixCount += 1
                    if (simType != 'noTime'):
                        pvcPipeAges[simType][index] = 0
                else:
                    pipeDisable(pvcPipesList, pvcTriggerList,
                                index, periodCount, simType)
            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect <= 0:
                    indexSelect = 0
                indexSelect += 30 * \
                    int(math.trunc(float(pvcPipeAges[simType][index])))

                if (float(pvcWeibullList[indexSelect]) > float(pvcPipeThresholdList[simType][index])):
                    pvcPipeAges[simType][index] = 0
                    pvcPipeThresholdList[simType][index] = float(
                        (np.random.uniform(0, 1, 1))[0])
                    pipeDisable(pvcPipesList, pvcTriggerList,
                                index, periodCount, simType)
                    pipeFailureFile = open(
                        ('{}_pvcPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    pvcFailureStatus[simType][index] = 44
                if (simType != 'noTime'):
                    pvcPipeAges[simType][index] = float(
                        pvcPipeAges[simType][index]) + biHourToYear

        for index, item in enumerate(ironPipesList):
            if (int(ironFailureStatus[simType][index]) != 0):
                ironFailureStatus[simType][index] = int(
                    ironFailureStatus[simType][index]) - 1
                if (int(ironFailureStatus[simType][index]) <= 0):
                    ironPipeFixCount = 0
                    while (ironPipeFixCount < 24):
                        pipeFix(ironPipesList, ironTriggerList,
                                index, ironPipeFixCount, simType)
                        ironPipeFixCount += 1
                else:
                    pipeDisable(ironPipesList, ironTriggerList,
                                index, periodCount, simType)
                if (simType != 'noTime'):
                    ironPipeAges[simType][index] = 0

            else:
                indexSelect = 0
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + \
                    (30 * int(math.trunc(float(ironPipeAges[simType][index]))))

                if (float(ironWeibullList[indexSelect]) > float(ironPipeThresholdList[simType][index])):
                    ironPipeAges[simType][index] = 0
                    ironPipeThresholdList[simType][index] = float(
                        (np.random.uniform(0, 1, 1))[0])
                    pipeDisable(ironPipesList, ironTriggerList,
                                index, periodCount, simType)
                    # Writing to the seperate failure statistics file
                    pipeFailureFile = open(
                        ('{}_ironPipeFail.txt').format(simType), 'a')
                    pipeFailureFile.write('%s %s\n' % (index, biHour))
                    pipeFailureFile.close()
                    # This is based off of the 88 hr repair time, can be
                    # changed to w/e
                    ironFailureStatus[simType][index] = 44
                if (simType != 'noTime'):
                    ironPipeAges[simType][index] = float(
                        ironPipeAges[simType][index]) + biHourToYear
        for index, item in enumerate(pumpList):
            if (int(pumpFailureStatus[simType][index]) != 0):
                pumpFailureStatus[simType][index] = int(
                    pumpFailureStatus[simType][index]) - 1
                pumpDisable(pumpList, mutedPumpList,
                            index, periodCount, simType)
                if (int(pumpFailureStatus[simType][index]) <= 0):
                    pumpFixCount = 0
                    while (pumpFixCount < 24):
                        pumpDisable(mutedPumpList, pumpList,
                                    index, pumpFixCount, simType)
                        pumpFixCount += 1
                    if (simType != 'noTime'):
                        pumpAgeList[simType][index] = 0

            else:
                indexSelect = (math.trunc(tasMaxACT) - 19)
                if indexSelect < 0:
                    indexSelect = 0
                indexSelect = indexSelect + \
                    (30 * int(math.trunc(float(pumpAgeList[simType][index]))))
                if float(pumpWeibullList[indexSelect]) > float(pumpThresholdList[simType][index]):
                    if (simType != 'noTime'):
                        pumpAgeList[simType][index] = 0
                    pumpThresholdList[simType][index] = float(
                        (np.random.uniform(0, 1, 1))[0])
                    pumpFailureFile = open(
                        ('{}_pumpFail.txt').format(simType), 'a')
                    pumpFailureFile.write('%s %s\n' % (index, biHour))
                    pumpFailureFile.close()
                    pumpDisable(pumpList, mutedPumpList,
                                index, periodCount, simType)
                    # This is based off of the 16 hr repair time, can be
                    # changed to w/e
                    pumpFailureStatus[simType][index] = 8
                if (simType != 'noTime'):
                    pumpAgeList[simType][index] = float(
                        pumpAgeList[simType][index]) + biHourToYear

        f = open('D:\\Austin_Michne\\tripleSim\\input\\%s\\NorthMarin_%s.inp' % (
            simType, periodCount), 'r')
        fi = open('D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.rpt' % (
            simType, biHour), 'w')

        # Initializes the files for encoding
        a = 'D:\\Austin_Michne\\tripleSim\\input\\%s\\NorthMarin_%s.inp' % (
            simType, periodCount)
        b = 'D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.rpt' % (
            simType, biHour)

        # Byte objects
        b_a = a.encode('UTF-8')
        b_b = b.encode('UTF-8')

        # Opens the toolkit

        epalib.ENopen(b_a, b_b, "")
        epalib.ENopenH()
        init_flag = ct.c_int(1)
        time = ct.pointer(ct.c_long(3600))
        # timestep = ct.pointer(ct.c_long(1))
        epalib.ENinitH(init_flag)
        # Does the hydraulic solving
        errorcode = epalib.ENrunH(time)
        print('errorcode: %s' % errorcode)
        nodeid = ct.c_char_p(str(ID).encode('utf-8'))
        nodeidx = ct.pointer(ct.c_int(0))
        nodevalue = ct.pointer(ct.c_float(0.0))

        errorcode = epalib.ENgetnodeindex(nodeid, nodeidx)
        if errorcode != 0:
            print(5, 'ERRORCODE is', errorcode)
        print('NODEID', nodeid.value.decode('utf-8'),
              'has NODEIDX', nodeidx.contents.value)

        errorcode = epalib.ENgetnodevalue(
            nodeidx.contents, ENnodeparam.BASEDEMAND, nodevalue)
        if errorcode != 0:
            print(6, 'ERRORCODE is', errorcode)
        print('EN_BASEDEMAND is', nodevalue.contents.value)

        errorcode = epalib.ENgetnodevalue(
            nodeidx.contents, ENnodeparam.DEMAND, nodevalue)
        if errorcode != 0:
            print(7, 'ERRORCODE is', errorcode)
        print('EN_DEMAND is', nodevalue.contents.value)

        epalib.ENcloseH()
        epalib.ENclose()

        # Saves the hydraulic results file
        # epalib.ENsaveH()
        # Reports the data from the previous run
        # epalib.ENreport()
        # epalib.ENclose()

        # Closes all of the files open during the simulation
        f.close()
        fi.close()

        parsingRpt('D:\\Austin_Michne\\tripleSim\\output\\%s\\NorthMarin_%s.rpt' % (
            simType, biHour), dbCursor, dbObject, biHour)
        biHour += 1
        epaCount += 1

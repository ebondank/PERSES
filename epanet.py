from ctypes import cdll
import math
import os
import sqlite3 as sql
from decimal import Decimal
import numpy as np
from supporting_windows_2_28_17 import triggerListCreation, pipeDisable, pipeFix, pumpDisable, pumpMuteListCreation

#Loading modules and information necessary for batching
epalib = cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')

databaseObject = sql.connect('D:\\Austin_Michne\\1_11_17\\testing.db')
databaseCursor = databaseObject.cursor()

pvcWeibullFile = open('D:\\Austin_Michne\\1_11_17\\pvcWeibullFixed.txt', 'r')
pvcWeibullList = pvcWeibullFile.read().splitlines()
pvcWeibullFile.close()

ironWeibullFile = open('D:\\Austin_Michne\\1_11_17\\ironWeibullFixed.txt', 'r')
ironWeibullList = ironWeibullFile.read().splitlines()
ironWeibullFile.close()

pumpWeibullFile = open('D:\\Austin_Michne\\1_11_17\\pumpWeibullFixed.txt', 'r')
pumpWeibullList = pumpWeibullFile.read().splitlines()
pumpWeibullFile.close()

tasFile = open('D:\\Austin_Michne\\1_11_17\\tasMaxBD.txt', 'r')
tasMaxACTList = tasFile.read().expandtabs().splitlines()
tasFile.close()

ironPipesFile = open('D:\\Austin_Michne\\1_11_17\\ironPipes.txt', 'r')
ironPipesList = ironPipesFile.read().expandtabs().splitlines()
ironPipesFile.close()
ironTriggerList = triggerListCreation(ironPipesList)


pvcPipesFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipes.txt', 'r')
pvcPipesList = pvcPipesFile.read().expandtabs().splitlines()
pvcPipesFile.close()
pvcTriggerList = triggerListCreation(pvcPipesList)


pumpFile = open('D:\\Austin_Michne\\1_11_17\\pumps.txt', 'r')
pumpList = pumpFile.read().expandtabs().splitlines()
pumpFile.close()
mutedPumpList = triggerListCreation(pumpList)

pvcAgeFile = open('D:\\Austin_Michne\\1_11_17\\pvcAgeFile.txt', 'r')
pvcPipeAges = pvcAgeFile.read().expandtabs().splitlines()
pvcAgeFile.close()

ironAgeFile = open('D:\\Austin_Michne\\1_11_17\\ironAgeFile.txt', 'r')
ironPipeAges = ironAgeFile.read().expandtabs().splitlines()
ironAgeFile.close()

pumpAgeFile = open('D:\\Austin_Michne\\1_11_17\\pumpAgeFile.txt', 'r')
pumpAgeList = pumpAgeFile.read().expandtabs().splitlines()
pumpAgeFile.close()

pvcFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\pvcFailureStatus.txt', 'r')
pvcFailureStatus = pvcFailureStatusFile.read().splitlines()
pvcFailureStatusFile.close()

ironFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\ironFailureStatus.txt', 'r')
ironFailureStatus = ironFailureStatusFile.read().splitlines()
ironFailureStatusFile.close()

pumpFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\pumpFailureStatus.txt', 'r')
pumpFailureStatus = pumpFailureStatusFile.read().splitlines()
pumpFailureStatusFile.close()

pumpThresholdFile = open('D:\\Austin_Michne\\1_11_17\\pumpThresholdFile.txt', 'r')
pumpThresholdList = pumpThresholdFile.read().splitlines()
pumpThresholdFile.close()

pvcPipeThresholdFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipeThresholdFile.txt', 'r')
pvcPipeThresholdList = pvcPipeThresholdFile.read().splitlines()
pvcPipeThresholdFile.close()

ironPipeThresholdFile = open('D:\\Austin_Michne\\1_11_17\\ironPipeThresholdFile.txt', 'r')
ironPipeThresholdList = ironPipeThresholdFile.read().splitlines()
ironPipeThresholdFile.close()

# End of the loading space

biHourToYear = float(.0002283105022831050228310502283105)
biHourt = 0

readCountFile = open('D:\\Austin_Michne\\1_11_17\\countKeeper.txt', 'r')
countList = readCountFile.read().expandtabs().splitlines()
readCountFile.close()
biHour = int(countList[0])

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
                # This is based off of the 88 hr repair time, can be changed to w/e
                pvcFailureStatus[index] = 44
            pvcPipeAges[index] = float(pvcPipeAges[index]) + biHourToYear

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
                pipeFailureFile = open('D:\\Austin_Michne\\1_11_18_ironPipeFail.txt', 'a')
                pipeFailureFile.write('%s %s\n' % (index, biHour))
                pipeFailureFile.close()
                # This is based off of the 88 hr repair time, can be changed to w/e
                ironFailureStatus[index] = 44
            ironPipeAges[index] = float(ironPipeAges[index]) + biHourToYear
    for index, item in enumerate(pumpList):
        if (int(pumpFailureStatus[index]) != 0):
            pumpFailureStatus[index] = int(pumpFailureStatus[index]) - 1
            pumpDisable(pumpList, mutedPumpList, index, periodCount)

            if (int(pumpFailureStatus[index]) == 0):
                pumpFixCount = 0
                while (pumpFixCount < 24):
                    pumpDisable(mutedPumpList, pumpList, index, pumpFixCount)
                    pumpFixCount += 1
                pumpAgeList[index] = 0

        else:
            indexSelect = (math.trunc(tasMaxACT) - 19)
            if indexSelect < 0:
                indexSelect = 0
            indexSelect = indexSelect + (30 * int(math.trunc(float(pumpAgeList[index]))))
            if float(pumpWeibullList[indexSelect]) > float(pumpThresholdList[index]):
                pumpAgeList[index] = 0
                pumpThresholdList[index] = (np.random.uniform(0, 1, 1))[0]
                pumpFailureFile = open('D:\\Austin_Michne\\1_11_18_pumpFail.txt', 'a')
                pumpFailureFile.write('%s %s\n' % (index, biHour))
                pumpFailureFile.close()
                pumpDisable(pumpList, mutedPumpList, index, periodCount)
                # This is based off of the 16 hr repair time, can be changed to w/e
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
    errorcode1 = epalib.ENopen(b_a, b_b, b_c)
    # Does the hydraulic solving
    errorcode3 = epalib.ENsolveH()
    # Saves the hydraulic results file
    errorcode6 = epalib.ENsaveH()
    # Reports the data from the previous run
    errorcode7 = epalib.ENreport()
    # Closes all of the files open during the simulation
    f.close()
    fi.close()
    fu.close()

    ReportFile = open('D:\\Austin_Michne\\1_11_17\\output\\NorthMarin_%s.rpt' % (biHour), 'r')
    ReadingReport = ReportFile.read().expandtabs().splitlines()
    ReportFile.close()

    for index, item in enumerate(ReadingReport):
        SortingData = ReadingReport[index].split()
        if any("Pump" in s for s in SortingData):
            continue
        if any("Page" in s for s in SortingData):
            continue
        if any("Pressure" in s for s in SortingData):
            continue
        if any("Node" in s for s in SortingData):
            continue
        if any(":" in s for s in SortingData):
            continue
        if any(".." in s for s in SortingData):
            continue
        if any("*" in s for s in SortingData):
            continue
        if not SortingData:
            continue
        if any("--" in s for s in SortingData):
            continue
        if any("Link" in s for s in SortingData):
            continue
        if any("Velocity" in s for s in SortingData):
            continue
        if any("Demand" in s for s in SortingData):
            continue
        if any("Results" in s for s in SortingData):
            continue
        SortingData.insert(0, str(biHour))
        try:
            if '.' not in SortingData[4]:
                try:
                    if 'Tank' or 'Reservoir' in SortingData[5]:
                        del SortingData[5]

                        databaseCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?, ?, ?)''', (SortingData[0], SortingData[1], SortingData[2], SortingData[3], SortingData[4]))

                except IndexError:

                    databaseCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?, ?, ?)''', (SortingData[0], SortingData[1], SortingData[2], SortingData[3], SortingData[4]))

        except IndexError:
            try:
                databaseCursor.execute('''INSERT INTO linkData VALUES (?, ?, ?, ?, ?)''', (SortingData[0], SortingData[1], SortingData[2], SortingData[3], SortingData[4]))
            except IndexError:

                    databaseCursor.execute('''INSERT INTO linkData VALUES (?, ?, ?, ?, ?)''', ('NO DATA', 'NO DATA', 'NO DATA', 'NO DATA', 'NO DATA'))
    databaseObject.commit()

    biHour += 1
    biHourt += 1

extCountFile = open('D:\\Austin_Michne\\1_11_17\\countKeeper.txt', 'w')
extCountFile.write('%s' % (biHour))
extCountFile.close()

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

pvcFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\pvcFailureStatus.txt', 'w')
pvcAgeFile = open('D:\\Austin_Michne\\1_11_17\\pvcAgeFile.txt', 'w')
pvcPipeThresholdFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipeThresholdFile.txt', 'w')
for index, item in enumerate(pvcPipeAges):
    pvcFailureStatusFile.write('%s\n' % pvcFailureStatus[index])
    pvcAgeFile.write('%s\n' % pvcPipeAges[index])
    pvcPipeThresholdFile.write('%s\n' % pvcPipeThresholdList[index])
pvcPipeThresholdFile.close()
pvcAgeFile.close()
pvcFailureStatusFile.close()

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

from supporting import triggerListCreation
import sqlite3 as sql

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

biHourToYear = float(.0002283105022831050228310502283105)
databaseObject = sql.connect('D:\\Austin_Michne\\1_11_17\\testing.db')
databaseCursor = databaseObject.cursor()
biHour = 0

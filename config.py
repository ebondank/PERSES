from supporting import triggerListCreation
import numpy as np

pvcPipeAges = {'real': [], 'noTemp': [], 'noTime': []}
ironPipeAges = {'real': [], 'noTemp': [], 'noTime': []}
pumpAgeList = {'real': [], 'noTemp': [], 'noTime': []}
pvcFailureStatus = {'real': [], 'noTemp': [], 'noTime': []}
ironFailureStatus = {'real': [], 'noTemp': [], 'noTime': []}
pumpFailureStatus = {'real': [], 'noTemp': [], 'noTime': []}
pvcPipeThresholdList = {'real': [], 'noTemp': [], 'noTime': []}
ironPipeThresholdList = {'real': [], 'noTemp': [], 'noTime': []}
pumpThresholdList = {'real': [], 'noTemp': [], 'noTime': []}

biHourToYear = float(.0002283105022831050228310502283105)
biHour = 0

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
tasMaxACTList = {'real': list(tasFile.read().expandtabs().splitlines()), 'noTime': list(tasFile.read().expandtabs().splitlines()), 'noTemp': list(np.repeat([22], 33000))}
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

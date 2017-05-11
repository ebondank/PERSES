import os
import sqlite3 as sql
import numpy as np
from epanet import epanet
import config

# TODO qwd

pvcPipesFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipes.txt', 'r')
pvcPipesList = pvcPipesFile.read().expandtabs().splitlines()
pvcPipesFile.close()

pumpFile = open('D:\\Austin_Michne\\1_11_17\\pumps.txt', 'r')
pumpList = pumpFile.read().expandtabs().splitlines()
pumpFile.close()

ironPipesFile = open('D:\\Austin_Michne\\1_11_17\\ironPipes.txt', 'r')
ironPipesList = ironPipesFile.read().expandtabs().splitlines()
ironPipesFile.close()

config.ironPipeAges['real'] = np.random.uniform(0, 85, len(ironPipesList))
config.ironPipeAges['noTemp'] = config.ironPipeAges['real']
config.ironPipeAges['noTime'] = config.ironPipeAges['real']

pvcCount = len(config.pvcPipesList)
config.pvcPipeAges['real'] = np.append(np.random.normal(40, 9, pvcCount - 20), np.random.normal(13, 3, 20))
config.pvcPipeAges['noTemp'] = config.pvcPipeAges['real']
config.pvcPipeAges['noTime'] = config.pvcPipeAges['real']

config.pumpAgeList['real'] = np.array([10, 25])
config.pumpAgeList['noTemp'] = config.pumpAgeList['real']
config.pumpAgeList['noTime'] = config.pumpAgeList['real']

for index, item in enumerate(config.pvcPipesList):
    config.pvcFailureStatus['real'].append(0)
    config.pvcPipeThresholdList['real'].append(np.random.uniform(0, 1, 1)[0])
config.pvcFailureStatus['noTemp'] = config.pvcFailureStatus['real']
config.pvcFailureStatus['noTime'] = config.pvcFailureStatus['real']
config.pvcPipeThresholdList['noTemp'] = config.pvcPipeThresholdList['real']
config.pvcPipeThresholdList['noTime'] = config.pvcPipeThresholdList['real']

for index, item in enumerate(config.ironPipesList):
    config.ironFailureStatus.append(0)
    config.ironPipeThresholdList.append(np.random.uniform(0, 1, 1)[0])
config.ironFailureStatus['noTemp'] = config.ironFailureStatus['real']
config.ironFailureStatus['noTime'] = config.ironFailureStatus['real']
config.ironPipeThresholdList['noTemp'] = config.ironPipeThresholdList['real']
config.ironPipeThresholdList['noTime'] = config.ironPipeThresholdList['real']

for index, item in enumerate(config.pumpAgeList):
    config.pumpFailureStatusFile.append(0)
    config.pumpThresholdFile.append(np.random.uniform(0, 1, 1)[0])
config.pumpFailureStatus['noTemp'] = config.pumpFailureStatus['real']
config.pumpFailureStatus['noTime'] = config.pumpFailureStatus['real']
config.pumpThresholdList['noTemp'] = config.pumpThresholdList['real']
config.pumpThresholdList['noTime'] = config.pumpThresholdList['real']

# Creating all three databases
databaseObjectReal = sql.connect(('D:\\Austin_Michne\\tripleSim\\realistic{}.db').format(os.environ['SIMCOUNT']))
databaseCursorReal = databaseObjectReal.cursor()
databaseCursorReal.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, DemandGPM real, Head real, Pressure real)''')
databaseCursorReal.execute('''CREATE TABLE linkData (Bihour_Count real, LinkID real, Flow real, Velocity real, Headloss real)''')
databaseObjectReal.close()

databaseObject_noTemp = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTemp{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTemp = databaseObject_noTemp.cursor()
databaseCursor_noTemp.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, DemandGPM real, Head real, Pressure real)''')
databaseCursor_noTemp.execute('''CREATE TABLE linkData (Bihour_Count real, LinkID real, Flow real, Velocity real, Headloss real)''')
databaseObject_noTemp.close()

databaseObject_noTime = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTime{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTime = databaseObject_noTime.cursor()
databaseCursor_noTime.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, DemandGPM real, Head real, Pressure real)''')
databaseCursor_noTime.execute('''CREATE TABLE linkData (Bihour_Count real, LinkID real, Flow real, Velocity real, Headloss real)''')
databaseObject_noTime.close()


batch = 0
while batch < 2525:
    epanet('real', databaseCursorReal, databaseObjectReal)
    epanet('noTemp', databaseCursor_noTemp, databaseObject_noTemp)
    epanet('noTime', databaseCursor_noTime, databaseObject_noTime)
    batch += 1
    print(batch)

os.environ['SIMCOUNT'] = str(int(os.environ['SIMCOUNT']) + 1)

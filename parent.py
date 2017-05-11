import os
import sqlite3 as sql
import numpy as np
import epanet
import config
import sys

# TODO Need to set env variables for server


pvcPipesFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipes.txt', 'r')
pvcPipesList = pvcPipesFile.read().expandtabs().splitlines()
pvcPipesFile.close()

pumpFile = open('D:\\Austin_Michne\\1_11_17\\pumps.txt', 'r')
pumpList = pumpFile.read().expandtabs().splitlines()
pumpFile.close()

ironPipesFile = open('D:\\Austin_Michne\\1_11_17\\ironPipes.txt', 'r')
ironPipesList = ironPipesFile.read().expandtabs().splitlines()
ironPipesFile.close()

config.ironPipeAges['real'] = list(np.random.uniform(0, 85, len(ironPipesList)))
config.ironPipeAges['noTemp'] = list(config.ironPipeAges['real'])
config.ironPipeAges['noTime'] = list(config.ironPipeAges['real'])

pvcCount = len(config.pvcPipesList)
config.pvcPipeAges['real'] = np.append(np.random.normal(40, 9, pvcCount - 20), np.random.normal(13, 3, 20))
config.pvcPipeAges['noTemp'] = list(config.pvcPipeAges['real'])
config.pvcPipeAges['noTime'] = list(config.pvcPipeAges['real'])

config.pumpAgeList['real'] = np.array([10, 25])
config.pumpAgeList['noTemp'] = list(config.pumpAgeList['real'])
config.pumpAgeList['noTime'] = list(config.pumpAgeList['real'])

for index, item in enumerate(config.pvcPipesList):
    config.pvcFailureStatus['real'].append(0)
    config.pvcPipeThresholdList['real'].append(np.random.uniform(0, 1, 1)[0])
config.pvcFailureStatus['noTemp'] = list(config.pvcFailureStatus['real'])
config.pvcFailureStatus['noTime'] = list(config.pvcFailureStatus['real'])
config.pvcPipeThresholdList['noTemp'] = list(config.pvcPipeThresholdList['real'])
config.pvcPipeThresholdList['noTime'] = list(config.pvcPipeThresholdList['real'])

for index, item in enumerate(config.ironPipesList):
    config.ironFailureStatus.append(0)
    config.ironPipeThresholdList.append(np.random.uniform(0, 1, 1)[0])
config.ironFailureStatus['noTemp'] = list(config.ironFailureStatus['real'])
config.ironFailureStatus['noTime'] = list(config.ironFailureStatus['real'])
config.ironPipeThresholdList['noTemp'] = list(config.ironPipeThresholdList['real'])
config.ironPipeThresholdList['noTime'] = list(config.ironPipeThresholdList['real'])

for index, item in enumerate(config.pumpAgeList):
    config.pumpFailureStatusFile.append(0)
    config.pumpThresholdFile.append(np.random.uniform(0, 1, 1)[0])
config.pumpFailureStatus['noTemp'] = list(config.pumpFailureStatus['real'])
config.pumpFailureStatus['noTime'] = list(config.pumpFailureStatus['real'])
config.pumpThresholdList['noTemp'] = list(config.pumpThresholdList['real'])
config.pumpThresholdList['noTime'] = list(config.pumpThresholdList['real'])

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
    epanet.epanet('real', databaseCursorReal, databaseObjectReal)
    epanet.epanet('noTemp', databaseCursor_noTemp, databaseObject_noTemp)
    epanet.epanet('noTime', databaseCursor_noTime, databaseObject_noTime)
    del epanet
    del sys.modules['epanet']
    import epanet
    batch += 1
    print(batch)

os.environ['SIMCOUNT'] = str(int(os.environ['SIMCOUNT']) + 1)

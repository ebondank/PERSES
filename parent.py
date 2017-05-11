import os
import sqlite3 as sql
import numpy as np
import epanet
from config import *
import sys

# TODO Need to set env variables for server
os.environ['SIMCOUNT'] = '0'

pvcPipesFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipes.txt', 'r')
pvcPipesList = pvcPipesFile.read().expandtabs().splitlines()
pvcPipesFile.close()

pumpFile = open('D:\\Austin_Michne\\1_11_17\\pumps.txt', 'r')
pumpList = pumpFile.read().expandtabs().splitlines()
pumpFile.close()

ironPipesFile = open('D:\\Austin_Michne\\1_11_17\\ironPipes.txt', 'r')
ironPipesList = ironPipesFile.read().expandtabs().splitlines()
ironPipesFile.close()

ironPipeAges['real'] = list(np.random.uniform(0, 85, len(ironPipesList)))
ironPipeAges['noTemp'] = list(ironPipeAges['real'])
ironPipeAges['noTime'] = list(ironPipeAges['real'])

pvcCount = len(pvcPipesList)
pvcPipeAges['real'] = np.append(np.random.normal(40, 9, pvcCount - 20), np.random.normal(13, 3, 20))
pvcPipeAges['noTemp'] = list(pvcPipeAges['real'])
pvcPipeAges['noTime'] = list(pvcPipeAges['real'])

pumpAgeList['real'] = np.array([10, 25])
pumpAgeList['noTemp'] = list(pumpAgeList['real'])
pumpAgeList['noTime'] = list(pumpAgeList['real'])

for index, item in enumerate(pvcPipesList):
    pvcFailureStatus['real'].append(0)
    pvcPipeThresholdList['real'].append(np.random.uniform(0, 1, 1)[0])
pvcFailureStatus['noTemp'] = list(pvcFailureStatus['real'])
pvcFailureStatus['noTime'] = list(pvcFailureStatus['real'])
pvcPipeThresholdList['noTemp'] = list(pvcPipeThresholdList['real'])
pvcPipeThresholdList['noTime'] = list(pvcPipeThresholdList['real'])

for index, item in enumerate(ironPipesList):
    ironFailureStatus['real'].append(0)
    ironPipeThresholdList['real'].append(np.random.uniform(0, 1, 1)[0])
ironFailureStatus['noTemp'] = list(ironFailureStatus['real'])
ironFailureStatus['noTime'] = list(ironFailureStatus['real'])
ironPipeThresholdList['noTemp'] = list(ironPipeThresholdList['real'])
ironPipeThresholdList['noTime'] = list(ironPipeThresholdList['real'])

for index, item in enumerate(pumpAgeList):
    pumpFailureStatus['real'].append(0)
    pumpThresholdList['real'].append(np.random.uniform(0, 1, 1)[0])
pumpFailureStatus['noTemp'] = list(pumpFailureStatus['real'])
pumpFailureStatus['noTime'] = list(pumpFailureStatus['real'])
pumpThresholdList['noTemp'] = list(pumpThresholdList['real'])
pumpThresholdList['noTime'] = list(pumpThresholdList['real'])

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
    epanet.epanet(biHour, 'real', databaseCursorReal, databaseObjectReal)
    epanet.epanet(biHour, 'noTemp', databaseCursor_noTemp, databaseObject_noTemp)
    epanet.epanet(biHour, 'noTime', databaseCursor_noTime, databaseObject_noTime)
    del epanet
    del sys.modules['epanet']
    import epanet
    batch += 1
    print(batch)

os.environ['SIMCOUNT'] = str(int(os.environ['SIMCOUNT']) + 1)

import os
import sqlite3 as sql
import numpy as np
from config import *
import epanet

# TODO Environment variables for server aren't persisting for some reason
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
ironPipeAges['noTime'] = list(np.repeat([65], len(ironPipesList)))

pvcCount = len(pvcPipesList)
pvcPipeAges['real'] = list(np.append(np.random.normal(40, 9, pvcCount - 20), np.random.normal(13, 3, 20)))
pvcPipeAges['noTemp'] = list(pvcPipeAges['real'])
pvcPipeAges['noTime'] = list(np.repeat([33], pvcCount))

pumpAgeList['real'] = np.array([10, 25])
pumpAgeList['noTemp'] = list(pumpAgeList['real'])
pumpAgeList['noTime'] = list([12, 12])

pvcFailureStatus['real'] = list(np.zeros(len(pvcPipesList)))
pvcPipeThresholdList['real'] = list(np.random.uniform(0, 1, len(pvcPipesList)))
pvcFailureStatus['noTemp'] = list(np.zeros(len(pvcPipesList)))
pvcFailureStatus['noTime'] = list(np.zeros(len(pvcPipesList)))
pvcPipeThresholdList['noTemp'] = list(pvcPipeThresholdList['real'])
pvcPipeThresholdList['noTime'] = list(pvcPipeThresholdList['real'])

ironFailureStatus['real'] = list(np.zeros(len(ironPipesList)))
ironPipeThresholdList['real'] = list(np.random.uniform(0, 1, len(ironPipesList)))
ironFailureStatus['noTemp'] = list(np.zeros(len(ironPipesList)))
ironFailureStatus['noTime'] = list(np.zeros(len(ironPipesList)))
ironPipeThresholdList['noTemp'] = list(ironPipeThresholdList['real'])
ironPipeThresholdList['noTime'] = list(ironPipeThresholdList['real'])

pumpFailureStatus['real'] = [0, 0]
pumpThresholdList['real'] = list(np.random.uniform(0, 1, len(pumpList)))
pumpFailureStatus['noTemp'] = [0, 0]
pumpFailureStatus['noTime'] = [0, 0]
pumpThresholdList['noTemp'] = list(pumpThresholdList['real'])
pumpThresholdList['noTime'] = list(pumpThresholdList['real'])

# Creating all three databases
databaseObjectReal = sql.connect(('D:\\Austin_Michne\\tripleSim\\realistic{}.db').format(os.environ['SIMCOUNT']))
databaseCursorReal = databaseObjectReal.cursor()
databaseCursorReal.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
# databaseCursorReal.execute('''CREATE TABLE linkData (Bihour_Count real, LinkID real, Flow real, Velocity real, Headloss real)''')


databaseObject_noTemp = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTemp{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTemp = databaseObject_noTemp.cursor()
databaseCursor_noTemp.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, DemandGPM real, Head real, Pressure real)''')
databaseCursor_noTemp.execute('''CREATE TABLE linkData (Bihour_Count real, LinkID real, Flow real, Velocity real, Headloss real)''')


databaseObject_noTime = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTime{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTime = databaseObject_noTime.cursor()
databaseCursor_noTime.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, DemandGPM real, Head real, Pressure real)''')
databaseCursor_noTime.execute('''CREATE TABLE linkData (Bihour_Count real, LinkID real, Flow real, Velocity real, Headloss real)''')


batch = 0
while batch < 2525:
    epanet.epanet(batch, 'real', databaseCursorReal, databaseObjectReal)
    batch += 1
    print(batch)

os.environ['SIMCOUNT'] = str(int(os.environ['SIMCOUNT']) + 1)

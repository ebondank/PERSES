import os
import sqlite3 as sql
import numpy as np
from epanet import epanet


pvcPipesFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipes.txt', 'r')
pvcPipesList = pvcPipesFile.read().expandtabs().splitlines()
pvcPipesFile.close()

pumpFile = open('D:\\Austin_Michne\\1_11_17\\pumps.txt', 'r')
pumpList = pumpFile.read().expandtabs().splitlines()
pumpFile.close()

ironPipesFile = open('D:\\Austin_Michne\\1_11_17\\ironPipes.txt', 'r')
ironPipesList = ironPipesFile.read().expandtabs().splitlines()
ironPipesFile.close()

ironPipeAges = np.random.uniform(0, 85, len(ironPipesList))
pvcCount = len(pvcPipesList)
pvcPipeAges = np.append(np.random.normal(40, 9, pvcCount - 20), np.random.normal(13, 3, 20))
pumpAgeList = np.array([10, 25])

pvcFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\pvcFailureStatus.txt', 'w')
pvcAgeFile = open('D:\\Austin_Michne\\1_11_17\\pvcAgeFile.txt', 'w')
pvcPipeThresholdFile = open('D:\\Austin_Michne\\1_11_17\\pvcPipeThresholdFile.txt', 'w')
for index, item in enumerate(pvcPipesList):
    pvcFailureStatusFile.write('0\n')
    pvcAgeFile.write('%s\n' % (pvcPipeAges[index]))
    pvcPipeThresholdFile.write('%s\n' % (np.random.uniform(0, 1, 1))[0])
pvcFailureStatusFile.close()
pvcAgeFile.close()
pvcPipeThresholdFile.close()

ironFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\ironFailureStatus.txt', 'w')
ironAgeFile = open('D:\\Austin_Michne\\1_11_17\\ironAgeFile.txt', 'w')
ironPipeThresholdFile = open('D:\\Austin_Michne\\1_11_17\\ironPipeThresholdFile.txt', 'w')
for index, item in enumerate(ironPipesList):
    ironFailureStatusFile.write('0\n')
    ironAgeFile.write('%s\n' % (ironPipeAges[index]))
    ironPipeThresholdFile.write('%s\n' % (np.random.uniform(0, 1, 1))[0])
ironFailureStatusFile.close()
ironAgeFile.close()
ironPipeThresholdFile.close()

pumpFailureStatusFile = open('D:\\Austin_Michne\\1_11_17\\pumpFailureStatus.txt', 'w')
pumpAgeFile = open('D:\\Austin_Michne\\1_11_17\\pumpAgeFile.txt', 'w')
pumpThresholdFile = open('D:\\Austin_Michne\\1_11_17\\pumpThresholdFile.txt', 'w')
for index, item in enumerate(pumpAgeList):
    pumpFailureStatusFile.write('0\n')
    pumpAgeFile.write('%s\n' % (pumpAgeList[index]))
    pumpThresholdFile.write('%s\n' % (np.random.uniform(0, 1, 1))[0])
pumpFailureStatusFile.close()
pumpAgeFile.close()
pumpThresholdFile.close()
try:
    os.remove('D:\\Austin_Michne\\1_11_17\\testing.db')
except IOError:
    print("There was no such file found")

databaseObject = sql.connect('D:\\Austin_Michne\\1_11_17\\testing.db')
databaseCursor = databaseObject.cursor()
databaseCursor.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, DemandGPM real, Head real, Pressure real)''')
databaseCursor.execute('''CREATE TABLE linkData (Bihour_Count real, LinkID real, Flow real, Velocity real, Headloss real)''')
databaseObject.close()
readCountFile = open('D:\\Austin_Michne\\1_11_17\\countKeeper.txt', 'w')
readCountFile.write('0')
readCountFile.close()

batch = 0
while batch < 2525:
    epanet()
    batch += 1
    print(batch)

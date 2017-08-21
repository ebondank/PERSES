import os
import numpy as np
import copy
import sqlite3 as sql

def fileReading(arrayOfString):

    returnArray = list()

    for index, item in enumerate(arrayOfString):
        simDict = {}

        file1 = open(("{}").format(arrayOfString[index]), 'r')
        fileText = file1.read().splitlines()
        file1.close()

        for idx, itm in enumerate(fileText):
            try:
                dataArray = itm.split(' ')
                if (dataArray[0] in simDict.keys()):
                    simDict[dataArray[0]].append(dataArray[1])
                else:
                    simDict[dataArray[0]] = [dataArray[1]]
            except IndexError as ex:
                print('qwd')
        
        returnArray.append(copy.copy(simDict))

    return returnArray

f = open('testing.txt', 'w')
# Path = '8-10-17/realistic0.db'
# db = sql.connect(Path)
# com = db.cursor()
# f1 = open('8-10-17/realfailure.txt', 'w')
# f2 = open('8-10-17/noTempfailure.txt', 'w')
# for item in com.execute('SELECT * FROM failureData ORDER BY Bihour_Count ASC'):
#     if item[2] == 'pvc':
#         f1.write(('{} {}\n').format(int(item[1]), int(item[0])))
dataSet = fileReading(['8-20-17/real_pumpFail.txt', '8-20-17/noTemp_pumpFail.txt'])
d1 = list(dataSet[1].keys())

for index, item in enumerate(dataSet[0].keys()):
    try:
        compArray = dataSet[0][item]
        d1CompArray = dataSet[1][item]
        for idx, itm in enumerate(compArray):
            try:
                f.write(str(float(d1CompArray[idx]) - float(compArray[idx])) + "\n")
            except IndexError as ex1:
                f.write('Failure mismatch')
    except IndexError as ex:
        print('wtf')

    f.write(('{} \n\n\n').format(item))
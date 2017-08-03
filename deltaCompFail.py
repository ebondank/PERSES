import os
import numpy as np
import copy

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

dataSet = fileReading(['7-20-17/noTime_yesCC_pvcPipeFail.txt', '7-20-17/noTime_noCC_pvcPipeFail.txt'])
d1 = list(dataSet[1].keys())
f = open('testing.txt', 'w')
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
def pipeDisable(pipeList, triggerList, index, Remainder):
    stringToFind = pipeList[index]
    stringToMute = triggerList[index]

    breakingPipeFile = open('D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (Remainder), 'r')
    fileToBreakList = breakingPipeFile.read().expandtabs().splitlines()
    breakingPipeFile.close()

    for idx, itm in enumerate(fileToBreakList):
        if itm == stringToFind:
            fileToBreakList[idx] = stringToMute

    newlyBrokenFile = open('D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (Remainder), 'w')
    for inx, ite in enumerate(fileToBreakList):
        newlyBrokenFile.write('%s\n' % fileToBreakList[inx])
    newlyBrokenFile.close()



def pipeFix(pipeList, triggerList, index, Remainder):
    stringToEnable = pipeList[index]
    stringToFind = triggerList[index]

    breakingPipeFile = open('D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (Remainder), 'r')
    fileToBreakList = breakingPipeFile.read().expandtabs().splitlines()
    breakingPipeFile.close()

    indexToDisableList = list()
    for idx, itm in enumerate(fileToBreakList):
        if itm == stringToFind:
            fileToBreakList[idx] = stringToEnable

    newlyBrokenFile = open('D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (Remainder), 'w')
    for inx, ite in enumerate(fileToBreakList):
        newlyBrokenFile.write('%s\n' % fileToBreakList[inx])
    newlyBrokenFile.close()



def triggerListCreation(inputList):
    triggerList = list()
    for index, item in enumerate(inputList):
        stringToMute = str(item)
        fixedString = stringToMute.replace('Open', 'Closed')
        triggerList.append(fixedString)

    return triggerList


def pumpMuteListCreation(inputList):
    triggerList = list()
    for index, item in enumerate(inputList):
        if ("SPEED 1" in item):
            newString = item.replace("SPEED 1", "SPEED 0")
            triggerList.append(newString)

    return triggerList


def pumpDisable(pumpDependenciesList, pumpDependenciesMuteList, index, Remainder):
    stringToFind = pumpDependenciesList[index]
    stringToMute = pumpDependenciesMuteList[index]
    count1 = 0

    breakingPumpFile = open('D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (Remainder), 'r')
    fileToBreakList = breakingPumpFile.read().expandtabs().splitlines()

    breakingPumpFile.close()
    for idx, itm in enumerate(fileToBreakList):
        if (itm == (stringToFind)):
            fileToBreakList[idx] = stringToMute

    newlyBrokenFile = open('D:\\Austin_Michne\\1_11_17\\NorthMarin_%s.inp' % (Remainder), 'w')
    for inx, ite in enumerate(fileToBreakList):
        newlyBrokenFile.write('%s\n' % fileToBreakList[inx])
    newlyBrokenFile.close()

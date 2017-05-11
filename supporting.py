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


def parsingRpt(fileName, databaseCur, databaseObj, biHour):
    ReportFile = open(fileName, 'r')
    ReadingReport = ReportFile.read().expandtabs().splitlines()
    ReportFile.close()

    for index, item in enumerate(ReadingReport):
        SortingData = ReadingReport[index].split()
        if any("Pump" in s for s in SortingData):
            continue
        if any("Page" in s for s in SortingData):
            continue
        if any("Pressure" in s for s in SortingData):
            continue
        if any("Node" in s for s in SortingData):
            continue
        if any(":" in s for s in SortingData):
            continue
        if any(".." in s for s in SortingData):
            continue
        if any("*" in s for s in SortingData):
            continue
        if not SortingData:
            continue
        if any("--" in s for s in SortingData):
            continue
        if any("Link" in s for s in SortingData):
            continue
        if any("Velocity" in s for s in SortingData):
            continue
        if any("Demand" in s for s in SortingData):
            continue
        if any("Results" in s for s in SortingData):
            continue
        SortingData.insert(0, str(biHour))
        try:
            if '.' not in SortingData[4]:
                try:
                    if 'Tank' or 'Reservoir' in SortingData[5]:
                        del SortingData[5]

                        databaseCur.execute('''INSERT INTO NodeData VALUES (?, ?, ?, ?, ?)''', (SortingData[0], SortingData[1], SortingData[2], SortingData[3], SortingData[4]))

                except IndexError:

                    databaseCur.execute('''INSERT INTO NodeData VALUES (?, ?, ?, ?, ?)''', (SortingData[0], SortingData[1], SortingData[2], SortingData[3], SortingData[4]))

        except IndexError:
            try:
                databaseCur.execute('''INSERT INTO linkData VALUES (?, ?, ?, ?, ?)''', (SortingData[0], SortingData[1], SortingData[2], SortingData[3], SortingData[4]))
            except IndexError:

                databaseCur.execute('''INSERT INTO linkData VALUES (?, ?, ?, ?, ?)''', ('NO DATA', 'NO DATA', 'NO DATA', 'NO DATA', 'NO DATA'))
    databaseObj.commit()

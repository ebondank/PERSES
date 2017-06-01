import sqlite3 as sql
import math
import os


Path = 'realistic0.db'
db = sql.connect(Path)
com = db.cursor()
ouCount = 0
ou2Count = 0
pipeFile = open(os.path.expanduser('~/Desktop/Untitled1.txt'), 'r')
pipeList = pipeFile.read().splitlines()
pipeFile.close()
demandList = list()
for index, item in enumerate(pipeList):
    curr = float(item.split()[2])
    iD = float(item.split()[0])
    if (curr > 0):
        demandList.append(iD)

dbOUCount = list()
dbOUCount2 = list()
timeStepCountList = list()
count = 0
infiniteCount = 0
while (infiniteCount < 20):
    dbOUCount.append(0)
    dbOUCount2.append(0)
    infiniteCount += 1
print(demandList)
yrList = list()
for row in com.execute('SELECT * FROM NodeData ORDER BY Bihour_Count ASC'):
    newItem = float(row[1])
    if (newItem in demandList):
        try:
            ouCount = dbOUCount[math.floor((row[0]) / 8760)]
            ou2Count = dbOUCount2[math.floor((row[0]) / 8760)]
        except Exception:
            dbOUCount.append(0)
            dbOUCount2.append(0)
            ouCount = 0
            ou2Count = 0

        if (float(row[2]) <= 60):
            ouCount += 1
            print(row)
            if (float(row[2]) <= 40):
                ou2Count += 1
                print(row)
        try:
            # print("Boi")
            dbOUCount[math.floor((row[0]) / 8760)] = ouCount
            dbOUCount2[math.floor((row[0]) / 8760)] = ou2Count

        except Exception:
            print(row, "Broken")

for item in dbOUCount:
    print(item)

for item in dbOUCount2:
    print(item)

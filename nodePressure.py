import sqlite3 as sql
import math


Path = 'noTemp0.db'
db = sql.connect(Path)
com = db.cursor()
ouCount = 0
ou2Count = 0

dbOUCount = list()
dbOUCount2 = list()
timeStepCountList = list()
count = 0
infiniteCount = 0
while (infiniteCount < 20):
    dbOUCount.append(0)
    dbOUCount2.append(0)
    infiniteCount += 1

yrList = list()
for row in com.execute('SELECT * FROM NodeData ORDER BY Bihour_Count ASC'):
    print(row)
    try:
        ouCount = dbOUCount[math.floor((row[0]) / 4380)]
        ou2Count = dbOUCount2[math.floor((row[0]) / 4380)]
    except Exception:
        dbOUCount.append(0)
        dbOUCount2.append(0)
        ouCount = 0
        ou2Count = 0

    if (float(row[2]) <= 40):
        ouCount += 1
        if (float(row[2]) <= 20):
            ou2Count += 1
    try:
        # print("Boi")
        dbOUCount[math.floor((row[0]) / 4380)] = ouCount
        dbOUCount2[math.floor((row[0]) / 4380)] = ou2Count

    except Exception:
        print(row)

for item in dbOUCount:
	print(item)

for item in dbOUCount2:
	print(item)

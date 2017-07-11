from config_c import *
import os
import sqlite3 as sql
import itertools

i = 0
os.remove('localTesting.db')
db = sql.connect('localTesting.db')
dbCursor = db.cursor()
dbCursor.execute('''CREATE TABLE NodeData (NodeID real, Pressure real)''')




while (i < (linkList.contents.value ** 2)):
    failureDec = list(('{0:b}').format(i))
    for index, item in enumerate(failureDec):
        epalib.ENsetlinkvalue(ct.c_int(index), ct.c_int(11), ct.c_float(item))
    epalib.ENrunH(time)
    intCount = 1
    while (intCount < nodeCount.contents.value):
        epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
        epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
        dbCursor.execute('''INSERT INTO NodeData VALUES (?, ?)''', ((nodeID.value).decode('utf-8'), nodeValue.contents.value))
        # print(('{} {} {} \n').format(biHour, nodeID.value, nodeValue.contents.value))
        intCount += 1

    db.commit()
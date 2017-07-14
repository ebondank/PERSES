import sqlite3 as sql
import os
import numpy as np
import ctypes as ct

################## EPANET initilization ##################
epalib = ct.cdll.LoadLibrary('D:\\Austin_Michne\\1_11_17\\epanet2mingw64.dll')

f = open('north_marin_c.inp', 'r')
fi = open('D:\\Austin_Michne\\tripleSim\\null.rpt', 'w')

# Initializes the files for encoding
a = 'north_marin_c.inp'
b = 'D:\\Austin_Michne\\tripleSim\\null.rpt'
# Byte objects
b_a = a.encode('UTF-8')
b_b = b.encode('UTF-8')
epalib.ENopen(b_a, b_b, "")
epalib.ENopenH()
timestep = ct.pointer(ct.c_long(7200))
time = ct.pointer(ct.c_long(0))
init_flag = ct.c_int(1)
epalib.ENinitH(init_flag)
##### Fetching node count #####
nodeCount = ct.pointer(ct.c_int(0))
epalib.ENgetcount(ct.c_int(0), nodeCount)
nodeValue = ct.pointer(ct.c_float(0.0))
nodeID = ct.c_char_p(('Testing purposes').encode('UTF-8'))
##### Fetching link count #####
linkList = ct.pointer(ct.c_int(0))
epalib.ENgetcount(ct.c_int(2), linkList)
linkCounter = 1


databaseObject = sql.connect(('D:\\Austin_Michne\\tripleSim\\nodePressure.db'))
databaseCursor = databaseObject.cursor()
databaseCursor.execute('''CREATE TABLE NodeData (failedLinkID real, NodeID real, Pressure real)''')


while (linkCounter < linkList.contents.value):
    linkIndex = ct.c_int(linkCounter)
    # For the first pipe out of pump 10
    linkID = ct.c_char_p(str(linkCounter).encode('utf-8'))
    epalib.ENgetlinkid(linkIndex, linkID)
    epalib.ENsetlinkvalue(linkIndex, ct.c_int(11), ct.c_float(0.0))
    epalib.ENrunH(time)
    intCount = 1
    while (intCount < nodeCount.contents.value):
        epalib.ENgetnodevalue(ct.c_int(intCount), ct.c_int(11), nodeValue)
        epalib.ENgetnodeid(ct.c_int(intCount), nodeID)
        databaseCursor.execute('''INSERT INTO NodeData VALUES (?, ?, ?)''', ((linkID.value).decode('utf-8'), (nodeID.value).decode('utf-8'), nodeValue.contents.value))
    epalib.ENsetlinkvalue(linkIndex, ct.c_int(11), ct.c_float(1.0))
    linkIndex += 1
    
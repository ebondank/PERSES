import os
import sqlite3 as sql
from config_c import *
import ctypes as ct

# TODO Environment variables for server aren't persisting for some reason

# Creating all three databases
epalib = ct.cdll.LoadLibrary('epanet2.dll')
databaseObjectReal = sql.connect(('D:\\Austin_Michne\\tripleSim\\realistic{}.db').format(os.environ['SIMCOUNT']))
databaseCursorReal = databaseObjectReal.cursor()
databaseCursorReal.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
databaseCursorReal.execute('''CREATE TABLE linkData (Bihour_Count real, NodeID real, Pressure real)''')

databaseObject_noTemp = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTemp{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTemp = databaseObject_noTemp.cursor()
databaseCursor_noTemp.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
databaseCursor_noTemp.execute('''CREATE TABLE linkData (Bihour_Count real, NodeID real, Pressure real)''')


databaseObject_noTime = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTime{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTime = databaseObject_noTime.cursor()
databaseCursor_noTime.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
databaseCursor_noTime.execute('''CREATE TABLE linkData (Bihour_Count real, NodeID real, Pressure real)''')

batch = 0

f = open('north_marin_c.inp', 'r')
fi = open('D:\\Austin_Michne\\tripleSim\\zz.rpt', 'w')

# Initializes the files for encoding
a = 'north_marin_c.inp'
b = 'D:\\Austin_Michne\\tripleSim\\zz.rpt'

# Byte objects
b_a = a.encode('UTF-8')
b_b = b.encode('UTF-8')

# Opens the toolkit
epalib.ENopen(b_a, b_b, "")
epalib.ENopenH()
timestep = ct.pointer(ct.c_long(7200))
time = ct.pointer(ct.c_long(0))
epalib.ENinitH(init_flag)
init_flag = ct.c_int(1)
nodeCount = ct.pointer(ct.c_int(0))
epalib.ENgetcount(ct.c_int(0), nodeCount)
nodeValue = ct.pointer(ct.c_float(0.0))
nodeID = ct.c_char_p(('Testing purposes').encode('UTF-8'))

while batch < 2525:
    epanet.epanet('real', databaseCursorReal, databaseObjectReal)
    batch += 1
    print(batch)

epalib.ENcloseH()
epalib.ENclose()
os.environ['SIMCOUNT'] = str(int(os.environ['SIMCOUNT']) + 1)

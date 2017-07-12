import os
import sqlite3 as sql
from config_c import *
import epanet_c

# TODO Environment variables for server aren't persisting for some reason
# os.remove('D:\\Austin_Michne\\tripleSim\\realistic0.db')
# os.remove('D:\\Austin_Michne\\tripleSim\\noTime_yesCC0.db')
# os.remove('D:\\Austin_Michne\\tripleSim\\noTime_noCC0.db')
# os.remove('D:\\Austin_Michne\\tripleSim\\noTemp0.db')

failureFile = open('real_ironPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('real_pvcPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('real_pumpFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_ironPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_pvcPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_pumpFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_noCC_ironPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_noCC_pvcPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_noCC_pumpFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_yesCC_ironPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_yesCC_pvcPipeFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
failureFile = open('noTime_yesCC_pumpFail.txt', 'w')
failureFile.write('\n\n\n')
failureFile.close()
# Creating all three database
databaseObjectReal = sql.connect(('D:\\Austin_Michne\\tripleSim\\realistic{}.db').format(os.environ['SIMCOUNT']))
databaseCursorReal = databaseObjectReal.cursor()
databaseCursorReal.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
databaseCursorReal.execute('''CREATE TABLE linkData (Bihour_Count real, NodeID real, Pressure real)''')

databaseObject_noTime_yesCC = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTime_yesCC{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTime_yesCC = databaseObject_noTime_yesCC.cursor()
databaseCursor_noTime_yesCC.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
databaseCursor_noTime_yesCC.execute('''CREATE TABLE linkData (Bihour_Count real, NodeID real, Pressure real)''')

databaseObject_noTime_noCC = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTime_noCC{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTime_noCC = databaseObject_noTime_noCC.cursor()
databaseCursor_noTime_noCC.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
databaseCursor_noTime_noCC.execute('''CREATE TABLE linkData (Bihour_Count real, NodeID real, Pressure real)''')

databaseObject_noTime = sql.connect(('D:\\Austin_Michne\\tripleSim\\noTemp{}.db').format(os.environ['SIMCOUNT']))
databaseCursor_noTime = databaseObject_noTime.cursor()
databaseCursor_noTime.execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
databaseCursor_noTime.execute('''CREATE TABLE linkData (Bihour_Count real, NodeID real, Pressure real)''')

# Opens the toolkit

batch = 0
while batch < 83:
    epanet_c.epanet(batch, 'real', databaseCursorReal, databaseObjectReal)
    epanet_c.epanet(batch, 'noTemp', databaseCursor_noTime, databaseObject_noTime)
    epanet_c.epanet(batch, 'noTime_yesCC', databaseCursor_noTime_yesCC, databaseObject_noTime_yesCC)
    epanet_c.epanet(batch, 'noTime_noCC', databaseCursor_noTime_noCC, databaseObject_noTime_noCC)
    print(batch)
    batch += 1

epalib.ENcloseH()
epalib.ENclose()
os.environ['SIMCOUNT'] = str(int(os.environ['SIMCOUNT']) + 1)

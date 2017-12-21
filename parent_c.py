import os
import sqlite3 as sql
from config_c import *
import epanet_c

# Creating all the databases
simsToRun = ['real', 'noTemp', 'historical']
conn_dict = dict()
cursor_dict = dict()
for sim in simsToRun:
    for comp_type in threeSim.keys():
        f_ = open(('{}_{}_fail.txt').format(sim, comp_type), 'w')
        f_.close()
    try:
        os.remove(('{}.db').format(sim))
    except Exception as exp:
        print('No database here')
    conn_dict[sim] = sql.connect(('{}.db').format(sim))
    cursor_dict[sim] = conn_dict[sim].cursor()
    cursor_dict[sim].execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
    cursor_dict[sim].execute('''CREATE TABLE failureData (Bihour_Count real, NodeID real, componentType real)''')
batch = 0

while batch < 150:
    for sim in simsToRun:
        epanet_c.epanet(batch, sim, cursor_dict[sim], conn_dict[sim])
    print(batch)
    batch += 1

epalib.ENcloseH()
epalib.ENclose()
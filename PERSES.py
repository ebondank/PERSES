import os
import sqlite3 as sql
# All code in PERSES_configuration must be ran before PERSES can funtion, DO NOT alter this line
from PERSES_configuration import *
from PERSES_simulation import EPANET_simulation
import multiprocessing as mp

# Creating all the databases, failure files, and simulation parametes necessary
if __name__ == "__main__":
    simsToRun = ['real', 'noTemp', 'historical']
    conn_dict = dict()
    cursor_dict = dict()
    for sim in data.keys():
        for comp_type in data[sim].keys():
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

    # Doing batched simulations
    # TODO: Parallelize this code
    cursors = cursor_dict.values()
    conns = conn_dict.values()
    while batch < 150:
        pool = mp.Pool(len(simsToRun))
        sim_list = []
        for sim in simsToRun:
            sim_list.append(tuple([batch, sim]))
        res = pool.starmap(EPANET_simulation, sim_list)
        for index, output in enumerate(res):
            cursors[index].executemany('''INSERT INTO failureData VALUES (?, ?, ?)''', output['failure_data'])
            cursors[index].executemany('''INSERT INTO NodeData VALUES (?, ?, ?)''', output['node_data'])
            conns[index].commit()
        print(batch)
        batch += 1

    epalib.ENcloseH()
    epalib.ENclose()
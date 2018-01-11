import dill
import os
import sqlite3 as sql
import atexit
# All code in PERSES_configuration must be ran before PERSES can funtion, DO NOT alter this line
from PERSES_configuration import *
from PERSES_simulation import simulation
import multiprocessing as mp
import pathos

# def file_cleaning():
#     with os.scandir() as it:
#         for file in it:
#             if len(file.name().split('.')) > 1:
#                 os.remove(file.name)
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
    cursors = list(cursor_dict.values())
    conns = list(conn_dict.values())
    while batch < 150:
        # pool = mp.Pool(len(simsToRun))
        pool = pathos.pools.ProcessPool(len(simsToRun))
        sim_list = []
        res = []
        for sim in simsToRun:
            sim_item = simulation(batch, sim,data = data,time = time,tasMaxACTList =
            tasMaxACTList,nodeCount = nodeCount,nodeValue=nodeValue, nodeID = nodeID, normal_run_list = normal_run_list,distList =
            distList, timestep = timestep,biHourToYear = biHourToYear)
            sim_list.append(sim_item)
            # res.append(sim_item.EPANET_simulation())
        res = pool.map(simulation.EPANET_simulation, sim_list)
        pool.close()
        pool.join()
        for index in range(0, len(res)):
            cursors[index].executemany('''INSERT INTO failureData VALUES (?, ?, ?)''', res[index]['failure_data'])
            conns[index].commit()
            cursors[index].executemany('''INSERT INTO NodeData VALUES (?, ?, ?)''', res[index]['node_data'])
            conns[index].commit()
            # for item in sorted(list(res[index]['failure_data'].values()), key=lambda x: x[2])
            for comp in comps:
                write_list = res[index]['failure_data']
                write_list = filter(lambda x: x[2] == comp, write_list)
                with open(("{}_{}_fail.txt").format(simsToRun[index], comp), 'a') as handle:
                    for value in write_list:
                        handle.write(("{} {}\n").format(value[1], value[0]))
        print(batch)
        batch += 1
    for sim in simsToRun:
        data[sim]["epanet"].ENcloseH()
        data[sim]["epanet"].ENclose()

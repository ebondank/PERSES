import dill
import os
import sqlite3 as sql
import atexit
# All code in PERSES_configuration must be ran before PERSES can funtion, DO NOT alter this line
from PERSES_configuration import *
from PERSES_simulation import failure_simulation
# from pathos.multiprocessing import _ProcessPool as Pool
# import multiprocessing_on_dill as mp

# def file_cleaning():
#     with os.scandir() as it:
#         for file in it:
#             if len(file.name().split('.')) > 1:
#                 os.remove(file.name)
# Creating all the databases, failure files, and simulation parametes necessary
if __name__ == "__main__":
    # simsToRun = {'temp_curves': ['real'],\
                #  'rep_curves': [{'pipe':22, 'pump':4}, {'pipe':44, 'pump':8}, {'pipe':88, 'pump':16}]}

    conn_dict = dict()
    cursor_dict = dict()
    for sim in sim_list['temp_curves']:
        for comp_type in comps:
            for rep_time in sim_list['rep_times']:
                f_ = open(('{}_{}_{}_fail.txt').format(sim, comp_type, rep_time), 'w')
                f_.close()
        try:
            os.remove(('{}.db').format(sim))
        except Exception as exp:
            print('No database here')
        for rep_time in sim_list['rep_times']:
            sim_with_rep = ("{}_{}").format(sim, rep_time)
            conn_dict[sim_with_rep] = sql.connect(('{}.db').format(sim))
            cursor_dict[sim_with_rep] = conn_dict[sim].cursor()
            cursor_dict[sim_with_rep].execute('''CREATE TABLE NodeData (Bihour_Count real, NodeID real, Pressure real)''')
            cursor_dict[sim_with_rep].execute('''CREATE TABLE NodeDataVLow (Bihour_Count real, NodeID real, Pressure real)''')
            cursor_dict[sim_with_rep].execute('''CREATE TABLE NodeDataMLow (Bihour_Count real, NodeID real, Pressure real)''')
            cursor_dict[sim_with_rep].execute('''CREATE TABLE failureData (Bihour_Count real, NodeID real, componentType real)''')
    batch = 0

    # Doing batched simulations
    # TODO: Parallelize this code
    cursors = list(cursor_dict.values())
    conns = list(conn_dict.values())
    simulation_list = list()
    for var in sim_list['temp_curves']:
        for val in sim_list['rep_times']:
            sim_item = failure_simulation(batch, var,\
                data=data,\
                time=time,\
                tasMaxACTList=tasMaxACTList,\
                nodeCount=nodeCount,\
                nodeValue=nodeValue,\
                nodeID=nodeID,\
                normal_run_list=normal_run_list,\
                distList=distList,\
                timestep=timestep,\
                biHourToYear=biHourToYear,\
                pipe_rep_time=val['pipe'],\
                pump_rep_time=val['pump'])
            simulation_list.append(sim_item)
    while batch < 150:
        res = []
        for sim in simulation_list:
            res.append(sim.EPANET_simulation())
        for index in range(0, len(res)):
            cursors[index].executemany('''INSERT INTO failureData VALUES (?, ?, ?)''', res[index]['failure_data'])
            conns[index].commit()
            cursors[index].executemany('''INSERT INTO NodeData VALUES (?, ?, ?)''', res[index]['node_data'])
            conns[index].commit()
            cursors[index].executemany('''INSERT INTO NodeDataVLow VALUES (?, ?, ?)''', res[index]['node_data_sub_20'])
            conns[index].commit()
            cursors[index].executemany('''INSERT INTO NodeDataMLow VALUES (?, ?, ?)''', res[index]['node_data_sub_40'])
            conns[index].commit()
        for comp in comps:
            for temp in sim_list['temp_curves']:
                for rep_time in sim_list['rep_times']:
                    write_list = res[index]['failure_data']
                    write_list = filter(lambda x: x[2] == comp, write_list)
                    with open(("{}_{}_{}_fail.txt").format(temp, comp, rep_time), 'a') as handle:
                        for value in write_list:
                            handle.write(("{} {}\n").format(value[1], value[0]))
        print(batch)
        batch += 1
    for sim in data:
        data[sim]["epanet"].ENcloseH()
        data[sim]["epanet"].ENclose()

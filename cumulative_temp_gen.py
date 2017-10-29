import os
def creation_from_modes(mode, file_):
    f_ = open(file_, 'r')
    f_list = f_.read().splitlines()
    f_.close()

    lists = f_list.pop(0)
    lists = lists.split('\t')
    to_write = dict()
    tracking = list()
    for item in lists:
        rcp = item[-2:]
        if (rcp in to_write.keys()):
            to_write[rcp]['count'] += 1
        else:
            to_write[rcp] = {'count': 1, 'values': [], 'int_count': 0, 'max_val': 0, 'max_values':[], 'min_val': 100, 'min_values':[]}
        tracking.append(rcp)

    for item in f_list:
        vals = item.split('\t')
        # vals.pop(0)
        for index, item in enumerate(vals):
            rcp = tracking[index]
            if (to_write[rcp]['int_count'] < to_write[rcp]['count']) and (len(to_write[rcp]['values']) != 0):
                to_write[rcp]['int_count'] += 1
                to_write[rcp]['values'][-1] += float(vals[index])
                if (float(vals[index])) > to_write[rcp]['max_val']:
                    to_write[rcp]['max_val'] = float(vals[index])
                elif (float(vals[index])) < to_write[rcp]['min_val']:
                    to_write[rcp]['min_val'] = float(vals[index])
            else:
                to_write[rcp]['max_values'].append(to_write[rcp]['max_val'])
                to_write[rcp]['min_values'].append(to_write[rcp]['min_val'])
                to_write[rcp]['int_count'] = 1
                to_write[rcp]['max_val'] = 0
                to_write[rcp]['min_val'] = 100
                to_write[rcp]['values'].append(float(vals[index]))
    
    for rcp in to_write.keys():
        f_ = open(('_{}_.txt').format(rcp), mode)
        f_min = open(('_{}_min.txt').format(rcp), mode)
        f_max = open(('_{}_max.txt').format(rcp), mode)
        for index, value in enumerate(to_write[rcp]["values"]):
            f_.write(('{}\n').format(float(float(value) / to_write[rcp]['count'])))
            f_min.write(('{}\n').format(to_write[rcp]["min_values"][index]))
            f_max.write(('{}\n').format(to_write[rcp]["max_values"][index]))
        f_.close()
        f_min.close()
        f_max.close()


creation_from_modes("w", '2015_2050.txt')
creation_from_modes("a", '2050_2099.txt')


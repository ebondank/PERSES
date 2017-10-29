import os
def creation_from_modes(mode, file_):
    f_ = open(file_, 'r')
    f_list = f_.read().splitlines()
    f_.close()

    # f_list.pop(0)
    lists = f_list.pop(0)
    lists = lists.split('\t')
    to_write = dict()
    tracking = list()
    for item in lists:
        name = (item.split('.'))[0]
        rcp = item[-2:]
        if (name in to_write.keys()):
            if (rcp in to_write[name].keys()):
                to_write[name][rcp]['count'] += 1
            else:
                to_write[name][rcp] = {'count': 1, 'values': [], 'int_count': 0}
        else:
            to_write[name] = {rcp: {'count': 1, 'values': [], 'int_count': 0}}
        tracking.append([name, rcp])

    for idx, item in enumerate(f_list):
        vals = item.split('\t')
        for index, item in enumerate(vals):
            name = tracking[index][0]
            rcp = tracking[index][1]
            if (to_write[name][rcp]['int_count'] < to_write[name][rcp]['count']) and (len(to_write[name][rcp]['values']) != 0):
                to_write[name][rcp]['int_count'] += 1
                to_write[name][rcp]['values'][-1] += float(vals[index])
            else:
                to_write[name][rcp]['int_count'] = 1
                to_write[name][rcp]['values'].append(float(vals[index]))

    for name in to_write.keys():
        for rcp in to_write[name].keys():
            f_ = open(('temp_output/{}_{}.txt').format(name, rcp), mode)
            for value in to_write[name][rcp]["values"]:
                f_.write(('{}\n').format(float(float(value) / to_write[name][rcp]['count'])))
            f_.close()

creation_from_modes("w", '2015_2050.txt')
creation_from_modes("a", '2050_2099.txt')
import numpy as np
import os

file1 = open(os.path.expanduser('7-4-17/noTime_pumpFail.txt'), 'r')
list1 = file1.read().splitlines()


file1.close()

yearList = list()
breakCount = list()
count = 0
while count < 83:
    yearList.append(count)
    breakCount.append(0)
    count += 1

for index, item in enumerate(list1):
    item = item.strip().split(' ')
    thisIndex = int(np.floor((int(item[1]) / 8760)))
    breakCount[thisIndex] = breakCount[thisIndex] + 1

for index, iteam in enumerate(breakCount):
    print(('{}\n').format(breakCount[index]))

import numpy as np
import os

file1 = open(os.path.expanduser('6-12-17/noTime_pumpFail.txt'), 'r')
list1 = file1.read().splitlines()
list1.pop()

file1.close()

yearList = list()
breakCount = list()
count = 0
while count < 35:
    yearList.append(count)
    breakCount.append(0)
    count += 1

for index, item in enumerate(list1):
    item = item.strip().split(' ')
    thisIndex = int(np.floor((int(item[1]) / 8760)))
    print(thisIndex)
    breakCount[thisIndex] = breakCount[thisIndex] + 1

for index, iteam in enumerate(breakCount):
    print(('{}\n').format(breakCount[index]))

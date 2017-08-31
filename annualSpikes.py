import os

tempInput = open('tasMaxBD85.txt', 'r')
tempList = tempInput.read().splitlines()
tempInput.close()

dayCount = 0
listOfSpikes = list()
for item in tempList:
    if (dayCount % 365 == 0):
        listOfSpikes.append(float(item))
        dayCount = 0

    if (float(item) > listOfSpikes[len(listOfSpikes) - 1]):
        listOfSpikes[len(listOfSpikes) - 1] = float(item)

    dayCount += 1
for item in listOfSpikes:
    print(item)
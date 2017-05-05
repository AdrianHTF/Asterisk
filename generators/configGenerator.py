from random import randint

TRUNK = "trunk"
TARGET = "target"
SIP_CONF = "sip.conf"
CALL_LIST = "callList"

DEFAULT_CONFIG ="[general]\n"

# fields for sip.conf
domains = []
users = []
secrets = []

# fields for callList
callList = []
trunkNames = []


def readTrunk(file):
    with open(file, "r")as input:
        for line in input:
            lines = line.split(',')
            print("lines: ", lines)
            domains.append(lines[0].rstrip('\n'))
            users.append(lines[1].rstrip('\n'))
            secrets.append(lines[2].rstrip('\n'))
    input.close()
    print(str(domains))
    print(str(users))
    print(str(secrets))


def writeSipConf(fileName):
    f = open(fileName, 'w+')
    createDefaultConfig(f)
    createRegisterConfig(f)
    createNumberConfig(f)
    f.close()


def createDefaultConfig(file):
    file.write(DEFAULT_CONFIG)


def createRegisterConfig(file):
    counter = 0
    for x in range(len(domains)):
        file.write('register => ' + users[counter] + ':' + secrets[counter] + '@' + domains[counter] + '\n')
        counter += 1


def createNumberConfig(file):
    counter = 0
    for x in range(len(domains)):
        trunkNames.append('number' + str(counter))
        file.write('\n[number' + str(counter) + ']\n' +
                    'host=' + str(domains[counter]) + '\n' +
                    'type=friend\n' +
                    'fromdomain=' + str(domains[counter]) + '\n' +
                    'disallow=all\n' +
                    'allow=ulaw\n' +
                    'allow=alaw\n' +
                    'dtmfmode=auto\n' +
                    'secret=' + str(secrets[counter]) + '\n' +
                    'defaultuser=' + str(users[counter]) + '\n' +
                    'trunkname=' + str(users[counter]) + '\n' +
                    'fromuser=' + str(users[counter]) + '\n')
        counter += 1


def readTargetFile(file):
    targetList = []
    with open(file, "r")as input:
        for line in input:
            lines = line.split(',')
            print("callLine: ", lines)
            targetList.append(lines)
    input.close()
    return targetList


def writeCallList(file, targetList):
    output = open(file, "w+")
    for item in targetList:
        protocol = item[0]
        target = item[1]
        min = int(item[2])
        max = int(item[3])
        total = int(item[4])
        numberCount = len(trunkNames)
        callCount = []
        if numberCount * max < total:
            print("not enough numbers or to low amount of maximal calls to manage total calls")
            break
        for x in range(numberCount):
            callCount.append(min)
        total = total - min * numberCount
        while total > 0:
            index = randint(0, numberCount - 1)
            distributeCalls(callCount, index, max)
            total -= 1
        print(callCount)
        for x in range(numberCount):
            output.write(protocol+'/'+trunkNames[x]+'/'+target+','+str(callCount[x])+'\n')
    output.close()


def distributeCalls(callCount, index, max):
    if callCount[index] < max:
        callCount[index] = callCount[index] + 1
    elif callCount[index] >= max:
        if index < len(callCount):
            index += 1
        else:
            index = 0
        distributeCalls(callCount, index, max)

        # def moveToSharedFolder(filename):
        # TODO add move to sharedFolder


targetList = readTargetFile(TARGET)
readTrunk(TRUNK)
writeSipConf(SIP_CONF)
writeCallList(CALL_LIST, targetList)
print(trunkNames)

import sys
import os
import subprocess
import time
import getopt

CALLLIST = "callList"
INITEXTENSION = ' extension 103@init-global-counter"'
EXTENSION = ' extension 102@name-record"'
COMMAND = '/usr/sbin/asterisk -rx "channel originate '
#callduration should be slightly higher than the real duration
CALLDURATION = 5
CALLWINDOW = 60

Calls = []
def main():
    replaceTarget = False
    replaceStart = False
    target = ""
    start = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:", ["target=", "start="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o in ("-t", "--target"):
            replaceTarget = True
            target = a
        elif o in ("-s", "--start"):
            replaceStart = True
            start = a

    print(str(replaceTarget))
    print("target: " + target)
    print(str(replaceStart))
    print("startAt: " + str(start))

    startTime = time.time()
    if replaceTarget:
        readCallListAndReplaceTarget(CALLLIST, target)
    else:
        readCallList(CALLLIST)
    call(int(start))
    totalTime = time.time() - startTime
    print("executing script took: " + str(totalTime) + "sec")

def readCallList(file):
    with open(file, "r")as input:
        for line in input:
            lines = line.rstrip('\n').split(',')
            call = [lines[0], int(lines[1])]
            Calls.append(call)
        print(Calls)
    input.close()

def readCallListAndReplaceTarget(file, target):
    with open(file, "r")as input:
        for line in input:
            lines = line.rstrip('\n').split(',')
            items = lines[0].split('/')
            newLine = items[0] + '/' + items[1] + '/' + target
            call = [newLine, int(lines[1])]
            Calls.append(call)
        print(Calls)
    input.close()


def calculateWaitTime(callDuration, callWindow, maxCalls, totalCalls):
    waitTime = 0
    if callWindow > maxCalls * callDuration:
        waitTime = (callWindow - maxCalls * callDuration) / totalCalls
    else:
        print("amount of calls in the given callWindow is not possible with the given callDuration and the amount of trunks")
        print("script now starts without waiting after each call and will last longer than the specified callWindow")
    return waitTime

def replaceTargets(list, target):
    for item in list:
        item[2] = target
    return

def setStart(start):
    callListIterationsDone = 0
    while start > 0:
        for call in Calls:
            if call[1] > 0:
                call[1] -= 1
                start -= 1
        callListIterationsDone += 1
    print(Calls)
    return callListIterationsDone

def call(start):
    totalCalls = 0
    maxCalls = 0
    numberCount = 0
    callsDone = 0
    for call in Calls:
        if call[1] > maxCalls:
            maxCalls = call[1]

        totalCalls += call[1]
        numberCount += 1

    waitTime = calculateWaitTime(CALLDURATION, CALLWINDOW, maxCalls, totalCalls)
    callListIterationsDone = setStart(int(start))
    maxCalls = maxCalls - callListIterationsDone
    print("waitTime: " + str(waitTime))
    print("totalCalls: " + str(totalCalls))
    print("amount of numbers: " + str(numberCount))
    for x in range(maxCalls):
        for call in Calls:
            if int(call[1]) > 0:
                call[1] = call[1] - 1
                callCommand = COMMAND + call[0] + EXTENSION
                #start call
                #subprocess.Popen(callCommand, shell=True)
                print(callCommand)
                print(call[1], x)
                callsDone += 1
                print("calls done: " + str(callsDone))
                time.sleep(waitTime)
        time.sleep(CALLDURATION)


if __name__ == '__main__':
    main()

import sys
import subprocess
import time
import getopt
from random import shuffle

CALLLIST = "callList"
INITEXTENSION = ' extension 103@init-global-counter"'
EXTENSION = ' extension 102@name-record"'
COMMAND = '/usr/sbin/asterisk -rx "channel originate '


Calls = []
def main():
    # callduration should be slightly higher than the real duration
    callDuration = 5
    # time the calls should be distributed in
    callWindow = 60
    replaceTarget = False
    target = ""
    start = 0
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:d:w:h", ["target=", "start=", "duration", "window", "help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o in ("-t", "--target"):
            replaceTarget = True
            target = a
            print("target: " + target)
        elif o in ("-s", "--start"):
            start = a
        elif o in ("-d", "--duration"):
            callDuration = int(a)
        elif o in ("-w", "--window"):
            callWindow = int(a)
        elif o in ("-h", "--help"):
            print("possible parameters are:\n" +
                  "-t <target>: replaces all numbers which are called with this target\n" +
                  "-s <start>: starts the script at the point where 'start' calls are already done\n" +
                  "-d <duration>: specifies the duration of a call\n" +
                  "-w <callwindow>: specifies the time in which the script executes the calls\n"
                  )

    print("startAt: " + str(start))

    startTime = time.time()
    if replaceTarget:
        readCallListAndReplaceTarget(CALLLIST, target)
    else:
        readCallList(CALLLIST)
    call(int(start), callDuration, callWindow)
    totalTime = time.time() - startTime
    print("executing script took: " + str(totalTime) + "sec")

def readCallList(file):
    with open(file, "r")as input:
        for line in input:
            lines = line.rstrip('\n').split(',')
            call = [lines[0], int(lines[1])]
            Calls.append(call)
    input.close()

def readCallListAndReplaceTarget(file, target):
    with open(file, "r")as input:
        for line in input:
            lines = line.rstrip('\n').split(',')
            items = lines[0].split('/')
            newLine = items[0] + '/' + items[1] + '/' + target
            call = [newLine, int(lines[1])]
            Calls.append(call)
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
    return callListIterationsDone

def call(start, callduration, callwindow):
    firstcall = True
    totalCalls = 0
    maxCalls = 0
    numberCount = 0
    callsDone = 0
    for call in Calls:
        if call[1] > maxCalls:
            maxCalls = call[1]

        totalCalls += call[1]
        numberCount += 1

    waitTime = calculateWaitTime(callduration, callwindow, maxCalls, totalCalls)
    callListIterationsDone = setStart(int(start))
    maxCalls = maxCalls - callListIterationsDone
    print("waitTime: " + str(waitTime))
    print("totalCalls: " + str(totalCalls))
    print("amount of numbers: " + str(numberCount))
    for x in range(maxCalls):
        for call in Calls:
            if int(call[1]) > 0:
                call[1] = call[1] - 1
                if firstcall:
                    callCommand = COMMAND + call[0] + INITEXTENSION
                    firstcall = False
                else:
                    callCommand = COMMAND + call[0] + EXTENSION
                #start call
                #subprocess.Popen(callCommand, shell=True)
                print("executing command: " + callCommand)
                callsDone += 1
                print("calls initiated: " + str(callsDone) + "\n")
                time.sleep(waitTime)
        shuffle(Calls)
        time.sleep(callduration)


if __name__ == '__main__':
    main()

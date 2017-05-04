import sys
import os
import subprocess
import time

CALLLIST = "callList"
INITEXTENSION = ' extension 103@init-global-counter"'
EXTENSION = ' extension 102@name-record"'
COMMAND = '/usr/sbin/asterisk -rx "channel originate '

#callduration should be slightly higher than the real duration
CALLDURATION = 5
CALLWINDOW = 60

Calls = []

def readCallList(file):
    with open(file, "r")as input:
        for line in input:
            lines = line.rstrip('\n').split(',')
            call = [lines[0], int(lines[1])]
            Calls.append(call)
        print(Calls)
    input.close()

def calculateWaitTime(callDuration, callWindow, maxCalls, totalCalls):
    waitTime = (callWindow - maxCalls * callDuration) / totalCalls
    return waitTime


def call():
    totalCalls = 0
    maxCalls = 0
    numberCount = 0
    for call in Calls:
        if call[1] > maxCalls:
            maxCalls = call[1]

        totalCalls += call[1]
        numberCount += 1

    waitTime = calculateWaitTime(CALLDURATION, CALLWINDOW, maxCalls, totalCalls)
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
                time.sleep(waitTime)
        time.sleep(CALLDURATION)


start = time.clock()
readCallList(CALLLIST)
call()
totalTime = time.clock() - start
print("executing skript took: " + str(totalTime) + "sec")

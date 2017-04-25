from asterisk import manager
import time
import os
import threading

HOST = '192.168.43.12'
PORT = 5038

inter_counter = 0

m = manager.Manager()

m.connect(HOST,port=PORT)
m.login('managerTest', 'ainesc')

targetURL = 'SIP/fonial/00491738156597'
targetURL_michi = 'SIP/fonial/004917696734058'
targetURL_stephan = 'SIP/fonial/004915141294170'
targetURL_adrian = 'SIP/fonial/004915111253810'

#for i in range(2):
#    if inter_counter == 0:
#        response = m.originate(targetURL, 103, context='init-global-counter', priority=1, async=True)
#        inter_counter += 1
#        print ("Global var initiated")
#    else:
#        response = m.originate(targetURL_stephan, 102, context='name-record', priority=1, async=True)
#        inter_counter += 1
#    print(m.status())
#a += 1
#variables['key'] = str(a)
#response2 = m.originate(targetURL_stephan, 102, context='name-record', priority=1, async=True, variables=variables)
#print(m.status())
response = m.originate(targetURL, 103, context='init-global-counter', priority=1, async=True)
print(m.status())

response = m.originate(targetURL_michi, 102, context='name-record', priority=1, async=True)
print(m.status())

response = m.originate(targetURL_stephan, 102, context='name-record', priority=1, async=True)
print(m.status())

response = m.originate(targetURL_adrian, 102, context='name-record', priority=1, async=True)
print(m.status())

m.close()

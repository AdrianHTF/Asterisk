configGenerator erzeugt aus den Files target und trunk die Files sip.conf und callList.

benoetigtes Format fuer trunk:
provider,username,secret
...
...

benoetigtes Format fuer target:
Protocol(SIP),targetNr,minCalls,maxCalls,totalCalls
...
...

erzeugtes Format sip.conf:
default config
registration of numbers
definition of trunks

erzeugtes Format callList:
"SIP/TrunkName/Target",Number of Calls
...
...

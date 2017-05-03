# README

## Manager Informations
If you want to use the manager outside the VM (e.g. python script) you should permit the incoming IP-Adress in the Asterisk Server. You can control the permissions over the GUI. After that you have to change the IP-Adress in the Python-Script too. 
Config datas should be manipulated over the Virtual-Box. 

### Things we need:
* VoiP-Provider in selected countries
* Accounts with Sip-datas to fill Sip.conf
* testing the script and look at the resources (Do we have enough?)
* Waiting time after each call from one number is not included right now
* Finish script

### Done right now:
* Asterisk call to different numbers
* Parallel calls over python script
* Call is recorded and saved into the shared folder of the Host-Guest-Machine
* A silent playback is called after the called one answered
* Records are saved with following format: Datetime, globalCounter
* Logging is included right now
* Scripts to generate SIP.conf is finished

### Other information:
* asterisk_conf have to be stored under following folder: /etc/asterisk/content of asterisk_conf
* In case of questions: Ask me, I am sitting next to you...

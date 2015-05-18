# Team 9    (Adelaide)
# 
# Jun Jen CHAN    (341759)
# Daniel TEH    (558424)
# Tou LEE    (656128)
# David MONROY    (610346)
# Jaime MARTINEZ    (642231)

# This code is used by the NeCTAR instances to replicate their CouchDB databases.
# Author: Jun Jen Chan

import socket
from subprocess import call

# reads list of instance IPs from the harvestIPs file
harvestIPs = open('/Deployment/harvestIPs')

# for instance to retrieve own IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ip_address = s.getsockname()[0]
s.close()

# for each instance, do a push replication to all other CouchDB databases
for line in harvestIPs :
    if line != ip_address+"\n":
        target_ip = (line.split('\n'))[0]
        data = '{"source": "tweets_adelaide", "target": "http://'+target_ip+':5984/tweets_adelaide", "create_target": true, "continuous": true}'
        call(['sudo','curl','-H','Content-Type:application/json','-X','POST','localhost:5984/_replicate','-d',data])

# Team 9	(Adelaide)
# 
# Jun Jen CHAN	(341759)
# Daniel TEH	(558424)
# Tou LEE	(656128)
# David MONROY	(610346)
# Jaime MARTINEZ	(642231)

# This code is used by the NeCTAR instances to include their IP addresses in Duck DNS.
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

i = 0
for line in harvestIPs :
    i += 1
    
    # instance 1 is called 'cccadelaide1'
    # instance 2 is called 'cccadelaide2'
    if line == ip_address+"\n" and i == 1 :
        input = '"https://www.duckdns.org/update?domains=cccadelaide'+str(i)+'&token=46423977-d07f-490b-9136-6ffe67fd736d&ip='+ip_address+'"'
        call(['curl','-k',input])

# Team 9	(Adelaide)
# 
# Jun Jen CHAN	(341759)
# Daniel TEH	(558424)
# Tou LEE	(656128)
# David MONROY	(610346)
# Jaime MARTINEZ	(642231)

# This code is used by the NeCTAR instances to execute their respective tweet harvesters.
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
    
    # instance 1 calls the North Adelaide harvester and the Search API harvester
    if line == ip_address+"\n" and i == 1 :
        call(['python','/Harvest-API/tweetharvester/harvester-stream.py','north','jimmy'])
                call(['python','/Harvest-API/tweetharvester/harvester-search.py'])
    # instance 2 calls the South Adelaide harvester
    elif line == ip_address+"\n" and i == 2 :
        call(['python','/Harvest-API/tweetharvester/harvester-stream.py','south','david'])

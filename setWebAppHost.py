# Team 9    (Adelaide)
# 
# Jun Jen CHAN    (341759)
# Daniel TEH    (558424)
# Tou LEE    (656128)
# David MONROY    (610346)
# Jaime MARTINEZ    (642231)

# This code is used by the NeCTAR instances to update their own IP in the Web Application file, 'requests.js'.
# Author: Jun Jen Chan

import socket
from subprocess import call

readFile = '/WebApp/public/controllers/requests.js'
writeFile = 'temp_requests.js'	# temp file to write changes to

read = open(readFile)
write = open(writeFile,'w')

# for instance to retrieve own IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ip_address = s.getsockname()[0]
s.close()

for line in read :
    # look for '//changeHostHere' marker
    if line.startswith('//changeHostHere') :
        # declare new host IP
        write.write('host = \"'+ip_address+'\" //set to local instance IP\n')
    else :
        write.write(line)

read.close()
write.close()

# overwrite older file
call(['mv', writeFile, readFile])

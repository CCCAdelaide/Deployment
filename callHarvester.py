import socket
from subprocess import call

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ip_address = s.getsockname()[0]
s.close()

harvestIPs = open('/Deployment/harvestIPs')
i = 0
for line in harvestIPs :
	i += 1
	if line == ip_address+"\n" and i == 1 :
		call(['python','/Harvest-API/tweetharvester/harvester-north.py'])
	elif line == ip_address+"\n" and i == 2 :
		call(['python','/Harvest-API/tweetharvester/harvester-south.py'])

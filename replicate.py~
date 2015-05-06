import socket
from subprocess import call

harvestIPs = open('harvestIPs')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ip_address = (s.getsockname()[0].split('\n'))[0]
s.close()

for line in harvestIPs :
	if line != ip_address :
		data = '{"source": "tweets_adelaide", "target": "http://'+ip_address+':5984/tweets_adelaide, "create_target": true, "continuous": true}'
		call(['sudo','curl','-H','Content-Type:application/json','-X','POST','localhost:5984/_replicate','-d',data])

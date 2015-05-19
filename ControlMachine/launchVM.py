# Team 9	(Adelaide)
# 
# Jun Jen CHAN	(341759)
# Daniel TEH	(558424)
# Tou LEE	(656128)
# David MONROY	(610346)
# Jaime MARTINEZ	(642231)

# This code is used by the control machine to launch instances on NeCTAR and to call the Ansible playbook for setting up the instances.
# Author: Jun Jen Chan

import time
import subprocess
import os
import boto
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
conn = boto.connect_ec2(aws_access_key_id='f0e153d37993442bb6ebcd8b2fc681e9',
aws_secret_access_key='4c318298791a496489a661e53ceceb34', is_secure=True, region=region,
port=8773,path='/services/Cloud',validate_certs=False)

instanceCount = 2   # number of instances launched
instanceType = 'm2.small'    # only use m2 types as volume /dev mount from directory is hard-coded
instanceImage = 'ami-000022b3'	# Ubuntu image
volumeSize = 10 # volume size in Gb
instPlacement = 'melbourne-qh2-uom'
volPlacement = 'melbourne-qh2'
securityGroups = ['couchdb','default','http','ssh','WebApp']
private_key_name = 'group'
private_key_file = 'group.pem'

ticks = 10	# in seconds
time_before_running_ansible = 10	# in ticks

hosts = open('hosts', 'w')    # file to write instance IPs for ansible
harvestIPs = open('harvestIPs', 'w')    # file to write instace IPs for harvesting
hosts.write("[webservers]")

START = time.time()
for i in range(instanceCount) :
    print "Launching instance "+str(i+1)
    start = time.time()
    reservation = conn.run_instances(instanceImage,key_name=private_key_name,instance_type=instanceType,placement=instPlacement,security_groups=securityGroups)
    instance = reservation.instances[0]
    status = instance.update()

    # wait for instance to have a running status before attaching volume
    while status != 'running':
        end = time.time()
        print "Instance "+str(i+1)+" status: "+status+" (Time elapsed: %.2f s)" % (end-start)

        # recreate instance if it has an error status
        if status == 'error':
            print "Terminating instance "+str(i+1)
            instance.terminate()
            time.sleep(5)	# give time for previous instance to terminate to prevent exceeding Nectar VCPU limit

            print "Recreating instance "+str(i+1)
            reservation = conn.run_instances(instanceImage,key_name=private_key_name,instance_type=instanceType,placement=instPlacement,security_groups=securityGroups)
#            counter += 1
            instance = reservation.instances[0]
            status = instance.update()
        
        time.sleep(10)
        status = instance.update()
        
    if status == 'running':
        end = time.time()
        print "Instance "+str(i+1)+" is running (Time taken: %.2f s)" % (end-start)
    
    print "Creating volume of size "+str(volumeSize)+" Gb"
    start = time.time()
    volume = conn.create_volume(volumeSize, volPlacement)
    status = volume.update()

    # wait for volume to have an available status before attaching them to an instance
    while status != 'available':
        end = time.time()
        print "Volume status: " +status+" (Time elapsed: %.2f s)" % (end-start)
        time.sleep(10)
        status = volume.update()

    if status == 'available':
        end = time.time()
        print "Volume is available (Time taken: %.2f s)" % (end-start)
        print "Attaching volume to instance "+str(i+1)
        conn.attach_volume(volume.id, instance.id, "/dev/sdx")

    # write instance IP address information into 'hosts' and 'harvestIPs' file for use by the Ansible playbook
    IP = instance.ip_address
    hosts.write("\nubuntu@"+IP+" ansible_ssh_private_key_file="+private_key_file)
    harvestIPs.write(IP+"\n")
    
    # prevent 'Offending ECDSA key' error when ansible attempts to connect to instance 
    #	by removing instance IP from ~/.ssh/known_hosts if it exists
    NULL = open(os.devnull, 'w')	# used to ignore error message if 'known_hosts' does not exist
    subprocess.call(['ssh-keygen','-f','~/.ssh/known_hosts','-R',IP], stdout=NULL, stderr=subprocess.STDOUT)

# prevent 'WARNING: UNPROTECTED PRIVATE KEY FILE!' error from occuring
subprocess.call(['chmod','600',private_key_file])

hosts.close()
harvestIPs.close()
END = time.time()
print "Completed launching of "+str(instanceCount)+" instances"
print "Total time taken: %.2f s" % (END-START)

# run a timer to allow instances to complete boot up and their SSH ports to be opened before calling the Ansible playbook
for i in range(time_before_running_ansible):
    print "Waiting "+str((time_before_running_ansible - i)*ticks)+" seconds for instances to complete launch..."
    time.sleep(ticks)

# call Ansible playbook
print "Calling Ansible playbook"
subprocess.call(['ansible-playbook','-s','ansible.yml'])

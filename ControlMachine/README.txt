To run the deployment scripts on the control machine, it requires the Python Boto (v2.34.0) library and the Ansible software to be installed. The following are the commands to install them on Ubuntu (for other operating systems please use their respective installation procedures):

For installing Boto:

$ sudo pip install --upgrade "boto<=2.34.0"

For installing Ansible:

$ sudo apt-get install software-properties-common
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get install ansible

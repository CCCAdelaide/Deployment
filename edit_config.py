from subprocess import call

input = open('/etc/couchdb/local.ini','r')
output = open('temp.ini','w')
for line in input.readlines():
    if line == "[couchdb]\n":
        output.write(line + "database_dir = /mnt/data/couchdb\n")
        output.write("view_index_dir = /mnt/data/couchdb\n")
    elif line == "[httpd]\n":
        output.write(line + "bind_address = 0.0.0.0\n")
    else:
        output.write(line)

call(['mv', 'temp.ini', '/etc/couchdb/local.ini'])

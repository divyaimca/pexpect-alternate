#!/usr/bin/python

import subprocess,select
import os, time, pty, sys


def waitFor(fd, substr):	
	#"poll the child for input"
	poll = select.poll()
	poll.register(fd, select.POLLIN)
	logFile = os.getcwd() + ‘/sshtest.log'
  while True:
     		evt = poll.poll()
     		data=os.read(fd, 1024)
      		print data
		with open(logFile, "a") as myfile:
     			myfile.write(data)
      		if substr in str(data):
       		  	return
      		if '(yes/no)' in str(data) or '[yes/no]' in str(data):
	  		os.write(fd,  "yes\n")


if len(sys.argv) < 5:
	raise Exception ('Insufficient number of arguments')
user = sys.argv[1]
host = sys.argv[2]
pwd = sys.argv[3]
sshCmd = sys.argv[4]
print sshCmd 
pid,fd = pty.fork()

if pid == 0:
    	cmd ='/usr/bin/ssh -o ServerAliveInterval=60 '+user+'@'+host
    	print cmd
    	subprocess.check_call(cmd, shell=True)    
else:
    	waitFor(fd, "password")
    	os.write(fd,  pwd+"\n")
    	waitFor(fd, "~]$")
    	os.write(fd, sshCmd+"\n")
    	waitFor(fd, "~]$")
    	os.write(fd,  "echo $? success\n")
    	os.write(fd,  "exit\n")
    	os.close(fd)

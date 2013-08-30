#!/bin/python
import sys
import telnetlib
from time import sleep
####################
HOST = "192.168.1.1"
USER = "admin"
PASS = "admin"
router = telnetlib.Telnet(HOST)
print HOST
#####################
try:
	router.read_until("Login: ", 2)
	router.write(USER + "\n")
	router.read_until(b"Password: ", 2)  
	router.write(PASS + "\n")
	print "Logging into " + HOST
	router.read_until(">", 2) 
	print "Logged in"
	print "Rebooting in 5 seconds...."
	#############################################
	for i in range(21):
		sys.stdout.write('\r')
		# the exact output you're looking for:
		sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
		sys.stdout.flush()
		sleep(0.25)
	#############################################
	router.write("reboot\n")
	print "\nReboot initiated"
	sleep(2)
except:
	print "Failed to login"
	exit()












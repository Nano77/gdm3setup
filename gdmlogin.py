#! /usr/bin/python2

import os
import sys
import getopt

CONF_PATH = "/etc/gdm/custom.conf"

#---
def SetValue(targetfile,targetsection,target,value):

	FIND_STATE = False

	ofile = open(targetfile,'r')
	lines = ofile.readlines()
	ofile.close()

	for i in range(len(lines)) :
		if lines[i].strip()[0:len(target)+1]==target+"=" :
			lines[i] = target+'='+value+'\n'

			FIND_STATE = True
			break

	if FIND_STATE :
		ofile = open(targetfile,'w')
		ofile.writelines(lines)
		ofile.close()
	else:
		
		SECTION_FIND_STATE = False
		
		for i in range(len(lines)) :
			if lines[i].strip()=="["+targetsection+"]" :
				lines.insert(i+1,target+'='+value+'\n')
				SECTION_FIND_STATE = True
				break

		if SECTION_FIND_STATE :
			ofile = open(targetfile,'w')
			ofile.writelines(lines)
			ofile.close()
		else:
			lines.append("\n")
			lines.append("["+targetsection+"]\n")
			lines.append(target+'='+value+'\n')
			lines.append("\n")
			ofile = open(targetfile,'w')
			ofile.writelines(lines)
			ofile.close()


#--

args = sys.argv[1:]

optlist, optargs = getopt.getopt(args,'mau:d:')

MANUALLOGIN = False
AUTOLOGIN = False
TIMED = False
TIME = 0
USER = False
USER_NAME = ""

for i in range(len(optlist)) :
	opt , arg = optlist[i]
	if opt == "-m" :
		MANUALLOGIN = True
	elif opt == "-a" :
		AUTOLOGIN = True
	elif opt == "-u" :
		USER = True
		USER_NAME = arg
	elif opt == "-d" :
		TIMED = True
		TIME = arg

if os.getuid()==0 :


	if not os.path.isfile(CONF_PATH) :

		ofile = open(CONF_PATH,'w')
		ofile.write("# GDM configuration storage\n\n\
[daemon]\n\n\
[security]\n\n\
[xdmcp]\n\n\
[greeter]\n\n\
[chooser]\n\n\
[debug]\n\n\
")
		ofile.close()

	if (MANUALLOGIN and AUTOLOGIN) or (AUTOLOGIN and not USER) or (not AUTOLOGIN and not MANUALLOGIN):
		if MANUALLOGIN and AUTOLOGIN :
			print >> sys.stderr, "ERROR : Manual and Automatic Login in same time !"
		if AUTOLOGIN and not USER :
			print >> sys.stderr, "ERROR : Automatic Login Without User Name !"
		if not AUTOLOGIN and not MANUALLOGIN :
			print "gdmlogin.py :\n\
 -m :\tManual login\n\
 -a :\tAutomtic login\n\
 -u :\tUserName (Need for autologin)\n\
 -d :\tDelay before autologin in second"

	else:
		if AUTOLOGIN :
			if AUTOLOGIN and not TIMED :
				print "AutomaticLoginEnable=1"
				print "AutomaticLogin="+USER_NAME
				print "TimedLoginEnable=0"
				SetValue(CONF_PATH,"daemon","AutomaticLoginEnable","1")
				SetValue(CONF_PATH,"daemon","AutomaticLogin",USER_NAME)
				SetValue(CONF_PATH,"daemon","TimedLoginEnable","0")
			else:
				print "AutomaticLoginEnable=0"
				print "TimedLoginEnable=1"
				print "TimedLogin="+USER_NAME
				print "TimedLoginDelay : "+ TIME
				SetValue(CONF_PATH,"daemon","AutomaticLoginEnable","0")
				SetValue(CONF_PATH,"daemon","TimedLoginEnable","1")
				SetValue(CONF_PATH,"daemon","TimedLogin",USER_NAME)
				SetValue(CONF_PATH,"daemon","TimedLoginDelay",TIME)
		else:
			print "AutomaticLoginEnable=0"
			print "TimedLoginEnable=0"
			SetValue(CONF_PATH,"daemon","AutomaticLoginEnable","0")
			SetValue(CONF_PATH,"daemon","TimedLoginEnable","0")
else:
	print >> sys.stderr, "Must Be Run as root"



#! /usr/bin/python2
# -*- coding: <utf-8> -*-

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import subprocess
import os
from gi.repository import GObject


subprocess.call("echo $LANG",shell=True)
LANG = os.environ['LANG']

loop = GObject.MainLoop()

def GetValue(target,default):
	targetfile = "/etc/gdm/custom.conf"
	ofile = open(targetfile,'r')
	lines = ofile.readlines()
	ofile.close()

	value = ""
	for i in range(len(lines)) :
		line = lines[i].strip()
		if line[0:len(target)+1]==target+"=" :
			value = line[len(target)+1:len(line)]
			break
		else:
			value=default
	return value

def str_to_bool(state) :
	if state.capitalize()=="True" or state=="1":
		b_state = True
	else :
		b_state = False

	return b_state

class GDM3SetupDBusService(dbus.service.Object):
	def __init__(self):
		bus=dbus.SystemBus()
		bus_name = dbus.service.BusName('apps.nano77.gdm3setup', bus)
		dbus.service.Object.__init__(self, bus_name, '/apps/nano77/gdm3setup')

	def policykit_test(self,sender,connexion,action):
		bus = dbus.SystemBus()
		proxy_dbus = connexion.get_object('org.freedesktop.DBus','/org/freedesktop/DBus/Bus', False)
		dbus_info = dbus.Interface(proxy_dbus,'org.freedesktop.DBus')
		sender_pid = dbus_info.GetConnectionUnixProcessID(sender)
		proxy_policykit = bus.get_object('org.freedesktop.PolicyKit1','/org/freedesktop/PolicyKit1/Authority',False)
		policykit_authority = dbus.Interface(proxy_policykit,'org.freedesktop.PolicyKit1.Authority')

		Subject = ('unix-process', {'pid': dbus.UInt32(sender_pid, variant_level=1),
						'start-time': dbus.UInt64(0, variant_level=1)})
		(is_authorized,is_challenge,details) = policykit_authority.CheckAuthorization(Subject, action, {'': ''}, dbus.UInt32(1), '') #, timeout=5000
		return is_authorized

	@dbus.service.method('apps.nano77.gdm3setup.set',in_signature='ss', out_signature='s',
					sender_keyword='sender', connection_keyword='connexion')
	def SetUI(self,name,value,sender=None, connexion=None):
		if self.policykit_test(sender,connexion,'apps.nano77.gdm3setup.set') :
			subprocess.call(unicode("su - gdm -s /bin/bash -c 'LANG="+LANG+" set_gdm.sh -n "+name+" -v "+'"'+value+'"'+"'"),shell=True)
			return "OK"
		else :
			return "ERROR : YOU ARE NOT ALLOWED !"

	@dbus.service.method('apps.nano77.gdm3setup.get','','as',sender_keyword='sender', connection_keyword='connexion')
	def GetUI(self,sender=None, connexion=None):
		subprocess.call("su - gdm -s /bin/sh -c 'LANG="+LANG+" get_gdm.sh'",shell=True)
		ifile = open("/tmp/GET_GDM",'r')
		settings = ifile.readlines()
		ifile.close()
		os.remove("/tmp/GET_GDM")
		return settings

	@dbus.service.method('apps.nano77.gdm3setup.set','bsbi','s',sender_keyword='sender', connection_keyword='connexion')
	def SetAutoLogin(self,AUTOLOGIN,USERNAME,TIMED,TIMED_TIME,sender=None, connexion=None):
		if self.policykit_test(sender,connexion,'apps.nano77.gdm3setup.set') :
			if AUTOLOGIN :
				if TIMED :
					subprocess.call("gdmlogin.py -a -u "+USERNAME+" -d "+str(int(TIMED_TIME)),shell=True)
				else:
					subprocess.call("gdmlogin.py -a -u "+USERNAME,shell=True)
			else:
				subprocess.call("gdmlogin.py -m",shell=True)
			return "OK"
		else :
			return "ERROR : YOU ARE NOT ALLOWED !"


	@dbus.service.method('apps.nano77.gdm3setup.get','','bsbi',sender_keyword='sender', connection_keyword='connexion')
	def GetAutoLogin(self,sender=None, connexion=None):

		AutomaticLoginEnable = str_to_bool(GetValue("AutomaticLoginEnable","False"))
		AutomaticLogin = GetValue("AutomaticLogin","")
		TimedLoginEnable = str_to_bool(GetValue("TimedLoginEnable","False"))
		TimedLogin = GetValue("TimedLogin","")
		TimedLoginDelay = GetValue("TimedLoginDelay","30")

		AUTOLOGIN = AutomaticLoginEnable or TimedLoginEnable
		TIMED = TimedLoginEnable
		TIMED_TIME = int(TimedLoginDelay)

		if AutomaticLoginEnable:
			USERNAME = AutomaticLogin

		if TimedLoginEnable:
			USERNAME = TimedLogin

		if not (AutomaticLoginEnable or TimedLoginEnable ):
			USERNAME = ""


		return AUTOLOGIN,USERNAME,TIMED,TIMED_TIME

	@dbus.service.method('apps.nano77.gdm3setup',sender_keyword='sender', connection_keyword='connexion')
	def stop(self,sender=None, connexion=None):
		loop.quit()


DBusGMainLoop(set_as_default=True)
myservice = GDM3SetupDBusService()
loop.run()

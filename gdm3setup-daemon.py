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

GDM_BIN_PATH="/usr/sbin/gdm"
GDM_CONF_PATH="/etc/gdm/custom.conf"
GDM_USER_NAME="gdm"

loop = GObject.MainLoop()

def GetValue(target,default):
	targetfile = GDM_CONF_PATH
	try:
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
	except IOError as (errno, strerror):
		value=default
	return value

def str_to_bool(state) :
	if state.capitalize()=="True" or state=="1":
		b_state = True
	else :
		b_state = False

	return b_state

def Get_Bus():
	ps_name=""
	address=""
	user_name=""
	dbus_pid=""
	dbus_address=""
	proclst = os.listdir('/proc')
	for ps in proclst:
		try:
			i = int(ps)
			ps_name = open('/proc/'+ps+'/comm').read().strip()

			if ps_name=="dbus-daemon":

				ofile = open('/proc/'+ps+'/environ','r')
				lines = ofile.read().split('\00')
				ofile.close()

				for ev in lines :
					if ev[0:len('DBUS_SESSION_BUS_ADDRESS')]=='DBUS_SESSION_BUS_ADDRESS':
						address = ev
					if ev[0:len('USERNAME')]=='USERNAME':
						user_name = ev

				if user_name=="USERNAME="+GDM_USER_NAME and address!="":
					dbus_address = address[len('DBUS_SESSION_BUS_ADDRESS')+1:len(address)]
					dbus_pid = ps

		except:
			i = 0

	return dbus_address,dbus_pid

def HackShellTheme(b):
	if b :
		os.rename('/usr/share/gnome-shell/theme','/usr/share/gnome-shell/theme.original')
		os.symlink('/usr/share/gnome-shell/theme.original','/usr/share/gnome-shell/theme')
		os.symlink('/usr/share/gnome-shell/theme.original','/usr/share/themes/Adwaita/gnome-shell')
	else :
		os.remove('/usr/share/themes/Adwaita/gnome-shell')
		os.remove('/usr/share/gnome-shell/theme')
		os.rename('/usr/share/gnome-shell/theme.original','/usr/share/gnome-shell/theme')

def Get_Shell_theme():
	if os.path.islink('/usr/share/gnome-shell/theme'):
		theme_path = os.readlink('/usr/share/gnome-shell/theme')
		if theme_path == '/usr/share/gnome-shell/theme.original':
			shell_theme='Adwaita'
		else :
			tb_path =  theme_path.split('/')
			shell_theme = tb_path[len(tb_path)-2]
	else :
		shell_theme='Adwaita'

	return shell_theme

def Set_Shell_theme(value):
	if value=='Adwaita':
		HackShellTheme(False)
	else:
		if not os.path.islink('/usr/share/gnome-shell/theme'):
			HackShellTheme(True)
		os.remove('/usr/share/gnome-shell/theme')
		os.symlink('/usr/share/themes/'+value+'/gnome-shell','/usr/share/gnome-shell/theme')

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

	@dbus.service.method('apps.nano77.gdm3setup',in_signature='ss', out_signature='s',
					sender_keyword='sender', connection_keyword='connexion')
	def SetUI(self,name,value,sender=None, connexion=None):
		if self.policykit_test(sender,connexion,'apps.nano77.gdm3setup.set') :
			if name!='SHELL_THEME':
				bus_adrress , bus_pid = Get_Bus()
				subprocess.call('su - '+GDM_USER_NAME+' -s /bin/bash -c "LANG='+LANG+' DBUS_SESSION_BUS_ADDRESS='+bus_adrress+' DBUS_SESSION_BUS_PID='+bus_pid+' set_gdm.sh -n '+name+' -v '+"'"+value+"'"+'"',shell=True)
			else :
				Set_Shell_theme(value)

			return "OK"
		else :
			return "ERROR : YOU ARE NOT ALLOWED !"

	@dbus.service.method('apps.nano77.gdm3setup','','as',sender_keyword='sender', connection_keyword='connexion')
	def GetUI(self,sender=None, connexion=None):
		subprocess.call("su - "+GDM_USER_NAME+" -s /bin/sh -c 'LANG="+LANG+" get_gdm.sh'",shell=True)
		ifile = open("/tmp/GET_GDM",'r')
		settings = ifile.readlines()
		ifile.close()
		os.remove("/tmp/GET_GDM")
		settings.append("SHELL='"+Get_Shell_theme()+"'\n")
		return settings

	@dbus.service.method('apps.nano77.gdm3setup','bsbi','s',sender_keyword='sender', connection_keyword='connexion')
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


	@dbus.service.method('apps.nano77.gdm3setup','','as',sender_keyword='sender', connection_keyword='connexion')
	def GetAutoLogin(self,sender=None, connexion=None):

		AutomaticLoginEnable = str_to_bool(GetValue("AutomaticLoginEnable","False"))
		AutomaticLogin = GetValue("AutomaticLogin","")
		TimedLoginEnable = str_to_bool(GetValue("TimedLoginEnable","False"))
		TimedLogin = GetValue("TimedLogin","")
		TimedLoginDelay = GetValue("TimedLoginDelay","30")

		AUTOLOGIN = str(AutomaticLoginEnable or TimedLoginEnable)
		TIMED = str(TimedLoginEnable)
		TIMED_TIME = TimedLoginDelay

		if AutomaticLoginEnable:
			USERNAME = AutomaticLogin

		if TimedLoginEnable:
			USERNAME = TimedLogin

		if not (AutomaticLoginEnable or TimedLoginEnable ):
			USERNAME = ""


		return AUTOLOGIN,USERNAME,TIMED,TIMED_TIME

	@dbus.service.method('apps.nano77.gdm3setup',sender_keyword='sender', connection_keyword='connexion')
	def StopDaemon(self,sender=None, connexion=None):
		loop.quit()


DBusGMainLoop(set_as_default=True)
myservice = GDM3SetupDBusService()
loop.run()

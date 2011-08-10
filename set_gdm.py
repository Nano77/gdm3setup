#! /usr/bin/env python2

import sys
import getopt
import os
import subprocess



args = sys.argv[1:]

try:
	optlist, optargs = getopt.getopt(args,'x',['GTK3_THEME=','ICON_THEME=','CURSOR_THEME=','WALLPAPER=','LOGO_ICON=','USER_LIST=','MENU_BTN=','BANNER=','BANNER_TEXT='])
except getopt.GetoptError, err:
	print str(err) 
	#usage()
	sys.exit(2)


for o,a in optlist:
	if  o  == "--GTK3_THEME":
		print "GTK3_THEME = " + a
		GTK3_THEME=a
	elif o == "--ICON_THEME":
		print "ICON_THEME = " + a 
		ICON_THEME = a 
	elif o == "--CURSOR_THEME":
		print "CURSOR_THEME = " + a 
		CURSOR_THEME = a 
	elif o == "--WALLPAPER":
		print "WALLPAPER = " + a 
		WALLPAPER = a 
	elif o == "--LOGO_ICON":
		print "LOGO_ICON = " + a 
		LOGO_ICON = a 
	elif o == "--USER_LIST":
		print "USER_LIST = " + a
		USER_LIST = a 
	elif o == "--MENU_BTN":
		print "MENU_BTN = " + a
		MENU_BTN = a 
	elif o == "--BANNER":
		print "BANNER = " + a 
		BANNER = a 
	elif o == "--BANNER_TEXT":
		print "BANNER_TEXT = " + a 
		BANNER_TEXT = a 
	else:
		print "???"



subprocess.call("gsettings set org.gnome.desktop.interface gtk-theme "+GTK3_THEME,shell=True)
subprocess.call("gsettings set org.gnome.desktop.interface icon-theme "+ICON_THEME,shell=True)
subprocess.call("gsettings set org.gnome.desktop.interface cursor-theme "+CURSOR_THEME ,shell=True)
subprocess.call("gsettings set org.gnome.desktop.background picture-uri 'file://"+WALLPAPER+"'",shell=True)

subprocess.call("gconftool-2 --type string --set /desktop/gnome/peripherals/mouse/cursor_theme '"+CURSOR_THEME+"'",shell=True)
subprocess.call("gconftool-2 --type string --set /apps/gdm/simple-greeter/logo_icon_name '"+LOGO_ICON+"'",shell=True)
subprocess.call("gconftool-2 --type bool --set /apps/gdm/simple-greeter/disable_user_list "+USER_LIST,shell=True)
subprocess.call("gconftool-2 --type bool --set /apps/gdm/simple-greeter/disable_restart_buttons "+MENU_BTN,shell=True)
subprocess.call("gconftool-2 --type bool --set /apps/gdm/simple-greeter/banner_message_enable "+BANNER,shell=True)
subprocess.call("gconftool-2 --type string --set /apps/gdm/simple-greeter/banner_message_text "+BANNER_TEXT,shell=True)
subprocess.call("gconftool-2 --type string --set /apps/gdm/simple-greeter/banner_message_text_nochooser "+BANNER_TEXT,shell=True)



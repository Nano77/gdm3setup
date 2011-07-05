#! /usr/bin/env python2

import os
import stat
import time
import subprocess
from gi.repository import Gtk

import gettext

import getpass

gettext.install("gdm3setup")

GTK3_THEME = "Zukitwo" 
ICON_THEME = "Faenza-Dark"
CURSOR_THEME = "Adwaita"
WALLPAPER = "/usr/share/backgrounds/gnome/Terraform-blue.jpg" 
LOGO_ICON = "distributor-logo"
USER_LIST = False
MENU_BTN = False

#-----------------------------------------------
def mainwin_close(event):
	Gtk.main_quit()

def load_gtk3_list():

	lst_themes = os.listdir('/usr/share/themes')

	for i in range(len(lst_themes)):
		if os.path.isdir('/usr/share/themes/'+lst_themes[i]+'/gtk-3.0') :
			ComboBox_gtk.append_text(lst_themes[i])

def load_icon_list():
	lst_icons = os.listdir('/usr/share/icons')

	for i in range(len(lst_icons)):
		if os.path.isdir('/usr/share/icons/'+lst_icons[i]+'/') :
			if 	os.path.isdir('/usr/share/icons/'+lst_icons[i]+'/cursors/') :
				ComboBox_cursor.append_text(lst_icons[i])
			else :
				ComboBox_icon.append_text(lst_icons[i])
		
def get_setting(name,data):
	value = None
	for line in data:
		if line[0:len(name)+1]==name+"=":
			value = line[len(name)+1:len(line)-1]

	return value	

def str_to_bool(state) :
	if state.capitalize()=="True" :
		b_state = True
	else :
		b_state = False		  

	return b_state

def get_iter(model,target):
	target_iter = None
	iter_test = model.get_iter_first()
	while iter_test!=None:
		name = model.get_value(iter_test,0)
		if "'"+name+"'" == target:
			target_iter = iter_test
			break 
		iter_test = model.iter_next(iter_test)
	return target_iter

def set_gdm(e):
	file1 = open(os.getcwd()+"/set_gdm.sh",'w')
	file1.write("su - gdm -s /bin/bash \n\
dbus-launch 2> /dev/null | grep DBUS_SESSION_BUS_ADDRESS > DBUS_SESSION_BUS_ADDRESS.FILE \n\
dbus-launch 2> /dev/null | grep DBUS_SESSION_BUS_PID > DBUS_SESSION_BUS_PID.FILE \n\
read DBUS_SESSION_BUS_ADDRESS_0 < DBUS_SESSION_BUS_ADDRESS.FILE \n\
read DBUS_SESSION_BUS_PID_0 < DBUS_SESSION_BUS_PID.FILE \n\
export $DBUS_SESSION_BUS_ADDRESS_0 \n\
export $DBUS_SESSION_BUS_PID_0 \n\
echo 'dbus adr : '$DBUS_SESSION_BUS_ADDRESS > test1\n\
echo 'dbus pid :'$DBUS_SESSION_BUS_PID\n\
gsettings set org.gnome.desktop.interface gtk-theme "+GTK3_THEME+" \n\
gsettings set org.gnome.desktop.interface icon-theme "+ICON_THEME+" \n\
gsettings set org.gnome.desktop.interface cursor-theme "+CURSOR_THEME+" \n\
gsettings set org.gnome.desktop.background picture-uri 'file://"+WALLPAPER+"' \n\
gconftool-2 --type string --set /apps/gdm/simple-greeter/logo_icon_name '"+LOGO_ICON+"'\n\
gconftool-2 --type bool --set /apps/gdm/simple-greeter/disable_user_list "+str(USER_LIST)+"\n\
gconftool-2 --type bool --set /apps/gdm/simple-greeter/disable_restart_buttons "+str(MENU_BTN))
	file1.close()

	file2 = open(os.getcwd()+"/call_set_gdm.sh",'w')
	file2.write("/bin/bash < "+os.getcwd()+"/set_gdm.sh\n\
echo 'call-set_gdm.sh'")
	file2.close()

	subprocess.call("chmod u+x "+os.getcwd()+"/call_set_gdm.sh",shell=True)
	subprocess.call("gksu "+os.getcwd()+"/call_set_gdm.sh",shell=True)

	os.remove(os.getcwd()+"/call_set_gdm.sh")
	os.remove(os.getcwd()+"/set_gdm.sh")

def get_gdm(e):
	file1 = open(os.getcwd()+"/get_gdm.sh",'w')
	file1.write('su - gdm -s /bin/bash \n\
dbus-launch 2> /dev/null | grep DBUS_SESSION_BUS_ADDRESS > DBUS_SESSION_BUS_ADDRESS.FILE \n\
dbus-launch 2> /dev/null | grep DBUS_SESSION_BUS_PID > DBUS_SESSION_BUS_PID.FILE \n\
read DBUS_SESSION_BUS_ADDRESS_0 < DBUS_SESSION_BUS_ADDRESS.FILE \n\
read DBUS_SESSION_BUS_PID_0 < DBUS_SESSION_BUS_PID.FILE \n\
export $DBUS_SESSION_BUS_ADDRESS_0 \n\
export $DBUS_SESSION_BUS_PID_0 \n\
echo -n "GTK="\n\
gsettings get org.gnome.desktop.interface gtk-theme \n\
echo -n "ICON="\n\
gsettings get org.gnome.desktop.interface icon-theme \n\
echo -n "CURSOR="\n\
gsettings get org.gnome.desktop.interface cursor-theme \n\
echo -n "BKG="\n\
gsettings get org.gnome.desktop.background picture-uri \n\
echo -n "LOGO="\n\
gconftool-2 --get /apps/gdm/simple-greeter/logo_icon_name\n\
echo -n "USER_LIST="\n\
gconftool-2 --get /apps/gdm/simple-greeter/disable_user_list\n\
echo -n "BTN="\n\
gconftool-2 --get /apps/gdm/simple-greeter/disable_restart_buttons\n\
')
	file1.close()

	subprocess.call("chmod a+x "+os.getcwd()+"/get_gdm.sh",shell=True) 

	file2 = open(os.getcwd()+"/call_get_gdm.sh",'w') 
	file2.write("/bin/bash < "+os.getcwd()+"/get_gdm.sh > /tmp/GDM_SETTINGS\n\
chown "+getpass.getuser()+" /tmp/GDM_SETTINGS\n")
	file2.close()
	
	subprocess.call("chmod u+x "+os.getcwd()+"/call_get_gdm.sh",shell=True)
	subprocess.call("gksu "+os.getcwd()+"/call_get_gdm.sh",shell=True)
	time.sleep(1)	
	file3 = open("/tmp/GDM_SETTINGS",'r')
	settings = file3.readlines()
	file3.close()

	os.remove(os.getcwd()+"/get_gdm.sh")
	os.remove(os.getcwd()+"/call_get_gdm.sh")
	os.remove("/tmp/GDM_SETTINGS")

	#---------------
	global WALLPAPER

	ComboBox_gtk.set_active_iter(get_iter(ComboBox_gtk.get_model(),get_setting("GTK",settings)))
	BKG = get_setting("BKG",settings)
	WALLPAPER = BKG[8:len(BKG)-1]
	FCB_bkg.set_filename(WALLPAPER)	
	ComboBox_icon.set_active_iter(get_iter(ComboBox_icon.get_model(),get_setting("ICON",settings)))
	ComboBox_cursor.set_active_iter(get_iter(ComboBox_cursor.get_model(),get_setting("CURSOR",settings)))
	Entry_logo.set_text(get_setting("LOGO",settings))
	CheckButton_user.set_active(str_to_bool(get_setting("USER_LIST",settings)))
 	CheckButton_restart.set_active(str_to_bool(get_setting("BTN",settings)))


def status_update():
	if(ComboBox_gtk.get_active_text()!=None and ComboBox_icon.get_active_text()!=None \
	and ComboBox_cursor.get_active_text()!=None and Entry_logo.get_text()!="" and FCB_bkg.get_filename()!=None):
		BTN_apply.set_sensitive(True)
	else:
		BTN_apply.set_sensitive(False)

def gtk3_theme_changed(e):
	global GTK3_THEME
	GTK3_THEME = ComboBox_gtk.get_active_text()
	print "GTK3 Theme Changed : " + GTK3_THEME
	status_update()

def wallpaper_changed(e):
	global WALLPAPER
	WALLPAPER = FCB_bkg.get_filename()
	print "Wallpaper Changed : " + WALLPAPER
	status_update()

def icon_theme_changed(e):
	global ICON_THEME
	ICON_THEME = ComboBox_icon.get_active_text()
	print "Icon Theme Changed : " + ICON_THEME
	status_update()

def cursor_theme_changed(e):
	global CURSOR_THEME
	CURSOR_THEME = ComboBox_cursor.get_active_text()
	print "Cursor Theme Changed : " + CURSOR_THEME
	status_update()

def logo_icon_changed(e):
	global LOGO_ICON
	LOGO_ICON = Entry_logo.get_text()
	print "Logo Icon Changed : " + LOGO_ICON
	status_update()

def user_list_toggled(e):
	global USER_LIST
	USER_LIST = CheckButton_user.get_active() 
	print "User List Changed : " + str(USER_LIST)


def menu_btn_toggled(e):
	global MENU_BTN
	MENU_BTN = CheckButton_restart.get_active() 
	print "Menu Btn Changed : " + str(MENU_BTN)

#-----------------------------------------------
mainwin = Gtk.Window()
mainwin.connect("destroy",mainwin_close)
mainwin.set_border_width(10)
mainwin.set_position(Gtk.WindowPosition.CENTER)
mainwin.set_resizable(False)
mainwin.set_title(_("GDM3 Setup"))
mainwin.set_icon_name("preferences-desktop-theme")

VBox_Main = Gtk.VBox.new(False, 0)
mainwin.add(VBox_Main)

HBox_gtk = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_gtk, False, True, 0)

Label_gtk = Gtk.Label(_("GTK3 theme"))
Label_gtk.set_alignment(0,0.5)
HBox_gtk.pack_start(Label_gtk, False, True, 0)

ComboBox_gtk =  Gtk.ComboBoxText.new()
ComboBox_gtk.connect("changed",gtk3_theme_changed)
HBox_gtk.pack_start(ComboBox_gtk, False, True, 0)

HBox_bkg = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_bkg, False, True, 0)

Label_bkg = Gtk.Label(_("Wallpaper"))
Label_bkg.set_alignment(0,0.5)
HBox_bkg.pack_start(Label_bkg, False, True, 0)

gettext.install("gtk30")
FCB_bkg = Gtk.FileChooserButton.new(_('Select a File'),Gtk.FileChooserAction.OPEN)
FCB_bkg.set_current_folder('/usr/share/backgrounds/gnome/')
filter_bkg = Gtk.FileFilter()
filter_bkg.add_pixbuf_formats()
filter_bkg.set_name('All images')
FCB_bkg.add_filter(filter_bkg)
FCB_bkg.connect("file-set",wallpaper_changed)
HBox_bkg.pack_end(FCB_bkg, False, True, 0)
gettext.install("gdm3setup")

HBox_icon = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_icon, False, True, 0)

Label_icon = Gtk.Label(_("Icon theme"))
Label_icon.set_alignment(0,0.5)
HBox_icon.pack_start(Label_icon, False, True, 0)

ComboBox_icon =  Gtk.ComboBoxText.new()
ComboBox_icon.connect("changed",icon_theme_changed)
HBox_icon.pack_start(ComboBox_icon, False, True, 0)

HBox_cursor = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_cursor, False, True, 0)

Label_cursor = Gtk.Label(_("Cursor theme"))
Label_cursor.set_alignment(0,0.5)
HBox_cursor.pack_start(Label_cursor, False, True, 0)

ComboBox_cursor =  Gtk.ComboBoxText.new()
ComboBox_cursor.connect("changed",cursor_theme_changed)
HBox_cursor.pack_start(ComboBox_cursor, False, True, 0)

HBox_logo = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_logo, False, True, 0)

Label_logo = Gtk.Label(_("Logo Icon"))
Label_logo.set_alignment(0,0.5)
HBox_logo.pack_start(Label_logo, False, True, 0)

Entry_logo =  Gtk.Entry()
Entry_logo.connect("changed",logo_icon_changed)
HBox_logo.pack_start(Entry_logo, False, True, 0)

HBox_user = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_user, False, True, 0)

CheckButton_user = Gtk.CheckButton(label=_("Disable User List"),use_underline=True)
CheckButton_user.connect("toggled",user_list_toggled)
HBox_user.pack_start(CheckButton_user, False, True, 0)

HBox_restart = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_restart, False, True, 0)

CheckButton_restart = Gtk.CheckButton(label=_("Disable Restart Buttons"),use_underline=True)
CheckButton_restart.connect("toggled",menu_btn_toggled)
HBox_restart.pack_start(CheckButton_restart, False, True, 0)

HBox9 = Gtk.HBox.new(True, 0)
VBox_Main.pack_end(HBox9, False, True, 0)

BTN_Load = Gtk.Button(_('Load'))
BTN_Load.connect("clicked",get_gdm)
HBox9.pack_start(BTN_Load, False, False, 0)

BTN_apply = Gtk.Button(_('Apply'))
BTN_apply.connect("clicked",set_gdm)
BTN_apply.set_sensitive(False)
HBox9.pack_start(BTN_apply, False, False, 0)


mainwin.show_all()

load_gtk3_list()
load_icon_list()

Gtk.main()

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
			ComboBox2.append_text(lst_themes[i])

def load_icon_list():
	lst_icons = os.listdir('/usr/share/icons')

	for i in range(len(lst_icons)):
		if os.path.isdir('/usr/share/icons/'+lst_icons[i]+'/') :
			ComboBox1.append_text(lst_icons[i])

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
gsettings set org.gnome.desktop.interface gtk-theme "+GTK3_THEME+" #Adwaita \n\
gsettings set org.gnome.desktop.interface icon-theme "+ICON_THEME+" #Adwaita \n\
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

	file2 = open(os.getcwd()+"/call_get_gdm.sh",'w') #echo 'call_get_gdm.sh' > TEST\n\ # \n\
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

	ComboBox2.set_active_iter(get_iter(ComboBox2.get_model(),get_setting("GTK",settings)))
	BKG = get_setting("BKG",settings)
	WALLPAPER = BKG[8:len(BKG)-1]
	FCB3.set_filename(WALLPAPER)	
	ComboBox1.set_active_iter(get_iter(ComboBox1.get_model(),get_setting("ICON",settings)))
	Entry4.set_text(get_setting("LOGO",settings))
	CheckButton5.set_active(str_to_bool(get_setting("USER_LIST",settings)))
 	CheckButton6.set_active(str_to_bool(get_setting("BTN",settings)))


def status_update():
	if(ComboBox2.get_active_text()!=None and ComboBox1.get_active_text()!=None \
	and Entry4.get_text()!="" and FCB3.get_filename()!=None):
		BTN9_2.set_sensitive(True)
	else:
		BTN9_2.set_sensitive(False)

def gtk3_theme_changed(e):
	global GTK3_THEME
	GTK3_THEME = ComboBox2.get_active_text()
	print "GTK3 Theme Changed : " + GTK3_THEME
	status_update()

def wallpaper_changed(e):
	global WALLPAPER
	WALLPAPER = FCB3.get_filename()
	print "Wallpaper Changed : " + WALLPAPER
	status_update()

def icon_theme_changed(e):
	global ICON_THEME
	ICON_THEME = ComboBox1.get_active_text()
	print "Icon Theme Changed : " + ICON_THEME
	status_update()

def logo_icon_changed(e):
	global LOGO_ICON
	LOGO_ICON = Entry4.get_text()
	print "Logo Icon Changed : " + LOGO_ICON
	status_update()

def user_list_toggled(e):
	global USER_LIST
	USER_LIST = CheckButton5.get_active() 
	print "User List Changed : " + str(USER_LIST)


def menu_btn_toggled(e):
	global MENU_BTN
	MENU_BTN = CheckButton6.get_active() 
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

HBox2 = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox2, False, True, 0)

Label2 = Gtk.Label(_("GTK3 theme"))
Label2.set_alignment(0,0.5)
HBox2.pack_start(Label2, False, True, 0)

ComboBox2 =  Gtk.ComboBoxText.new()
ComboBox2.connect("changed",gtk3_theme_changed)
HBox2.pack_start(ComboBox2, False, True, 0)

HBox3 = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox3, False, True, 0)

Label3_1 = Gtk.Label(_("Wallpaper"))
Label3_1.set_alignment(0,0.5)
HBox3.pack_start(Label3_1, False, True, 0)

gettext.install("gtk30")
FCB3 = Gtk.FileChooserButton.new(_('Select a File'),Gtk.FileChooserAction.OPEN)
FCB3.set_current_folder('/usr/share/backgrounds/gnome/')
filter3 = Gtk.FileFilter()
filter3.add_pixbuf_formats()
filter3.set_name('All images')
FCB3.add_filter(filter3)
FCB3.connect("file-set",wallpaper_changed)
HBox3.pack_end(FCB3, False, True, 0)
gettext.install("gdm3setup")

HBox1 = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox1, False, True, 0)

Label1 = Gtk.Label(_("Icon theme"))
Label1.set_alignment(0,0.5)
HBox1.pack_start(Label1, False, True, 0)

ComboBox1 =  Gtk.ComboBoxText.new()
ComboBox1.connect("changed",icon_theme_changed)
HBox1.pack_start(ComboBox1, False, True, 0)

HBox4 = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox4, False, True, 0)

Label4 = Gtk.Label(_("Logo Icon"))
Label4.set_alignment(0,0.5)
HBox4.pack_start(Label4, False, True, 0)

Entry4 =  Gtk.Entry()
Entry4.connect("changed",logo_icon_changed)
HBox4.pack_start(Entry4, False, True, 0)

HBox5 = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox5, False, True, 0)

CheckButton5 = Gtk.CheckButton(label=_("Disable User List"),use_underline=True)
CheckButton5.connect("toggled",user_list_toggled)
HBox5.pack_start(CheckButton5, False, True, 0)

HBox6 = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox6, False, True, 0)

CheckButton6 = Gtk.CheckButton(label=_("Disable Restart Buttons"),use_underline=True)
CheckButton6.connect("toggled",menu_btn_toggled)
HBox6.pack_start(CheckButton6, False, True, 0)

HBox9 = Gtk.HBox.new(True, 0)
VBox_Main.pack_end(HBox9, False, True, 0)

BTN9_1 = Gtk.Button('Load')
BTN9_1.connect("clicked",get_gdm)
HBox9.pack_start(BTN9_1, False, False, 0)

BTN9_2 = Gtk.Button('Apply')
BTN9_2.connect("clicked",set_gdm)
BTN9_2.set_sensitive(False)
HBox9.pack_start(BTN9_2, False, False, 0)


mainwin.show_all()

load_gtk3_list()
load_icon_list()

Gtk.main()

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
BANNER = False
BANNER_TEXT = "Wellcome"

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
	subprocess.call( \
	'gksu -D "GDM3Setup" "su - gdm -s /bin/sh -c '+"'"+'set_gdm.sh'+ \
	' --GTK3_THEME='+GTK3_THEME+ \
	' --ICON_THEME='+ICON_THEME+ \
	' --CURSOR_THEME='+CURSOR_THEME+ \
	' --WALLPAPER='+WALLPAPER+ \
	' --LOGO_ICON='+LOGO_ICON+ \
	' --USER_LIST='+str(USER_LIST)+ \
	' --MENU_BTN='+str(MENU_BTN)+ \
	' --BANNER='+str(BANNER)+ \
	' --BANNER_TEXT='+BANNER_TEXT \
	+"'"+'"' 
	,shell=True)

def get_gdm(e):
	p = subprocess.call('gksu -D "GDM3Setup" "su - gdm -s /bin/sh -c '+'get_gdm.sh'+' && chown '+getpass.getuser()+' /tmp/GET_GDM"',shell=True)

	file3 = open("/tmp/GET_GDM",'r')
	settings = file3.readlines()
	file3.close()
	os.remove("/tmp/GET_GDM")

	#---------------
	global WALLPAPER

	ComboBox_gtk.set_active_iter(get_iter(ComboBox_gtk.get_model(),get_setting("GTK",settings)))
	BKG = get_setting("BKG",settings)
	WALLPAPER = BKG[8:len(BKG)-1]
	FCB_bkg.set_filename(WALLPAPER)	
	ComboBox_icon.set_active_iter(get_iter(ComboBox_icon.get_model(),get_setting("ICON",settings)))
	ComboBox_cursor.set_active_iter(get_iter(ComboBox_cursor.get_model(),get_setting("CURSOR",settings)))
	Entry_logo.set_text(get_setting("LOGO",settings))
	CheckButton_banner.set_active(str_to_bool(get_setting("BANNER",settings)))
	Entry_banner_text.set_text(get_setting("BANNER_TEXT",settings))
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

def banner_toggled(e):
	global BANNER
	BANNER = CheckButton_banner.get_active()
	print "Banner Changed : " + str(BANNER)
	if BANNER :
		Entry_banner_text.set_sensitive(True)
	else:
		Entry_banner_text.set_sensitive(False)

def banner_text_changed(e):
	global BANNER_TEXT
	BANNER_TEXT = Entry_banner_text.get_text()
	print "Banner Text Changed : " + BANNER_TEXT
	status_update()

def user_list_toggled(e):
	global USER_LIST
	USER_LIST = CheckButton_user.get_active() 
	print "User List Changed : " + str(USER_LIST)


def menu_btn_toggled(e):
	global MENU_BTN
	MENU_BTN = CheckButton_restart.get_active() 
	print "Menu Btn Changed : " + str(MENU_BTN)

def autologin_clicked(e):
	win_autologin.show_all()

def Close_AutoLogin(e,data):
	win_autologin.hide()
	return True

def AutoLogin_toggled(e):
	if CheckButton_AutoLogin.get_active():
		HBox_username.set_sensitive(True)
		HBox_Delay.set_sensitive(True)
	else:
		HBox_username.set_sensitive(False)
		HBox_Delay.set_sensitive(False)

	if Entry_username.get_text()!="" or not CheckButton_AutoLogin.get_active():
		HBox_AutoLogin_Apply.set_sensitive(True)
	else:
		HBox_AutoLogin_Apply.set_sensitive(False)	

def username_changed(e):
	if Entry_username.get_text()!="":
		HBox_AutoLogin_Apply.set_sensitive(True)
	else:
		HBox_AutoLogin_Apply.set_sensitive(False)	

def Delay_toggled(e):
	if CheckButton_Delay.get_active():
		SpinButton_Delay.set_sensitive(True)
	else:
		SpinButton_Delay.set_sensitive(False)

def AutoLogin_Apply_clicked(e):
	AUTOLOGIN = CheckButton_AutoLogin.get_active()
	TIMED = CheckButton_Delay.get_active()
	TIMED_TIME = SpinButton_Delay.get_value()
	USERNAME = Entry_username.get_text()

	if AUTOLOGIN :
		if TIMED :
			subprocess.call("gksu -D 'GDM3Setup' 'gdmlogin.py -a -u "+USERNAME+" -d "+str(int(TIMED_TIME))+"'",shell=True)
		else:
			subprocess.call("gksu -D 'GDM3Setup' 'gdmlogin.py -a -u "+USERNAME+"'",shell=True)
	else:
		subprocess.call("gksu -D 'GDM3Setup' 'gdmlogin.py -m'",shell=True)

	win_autologin.hide()

#-----------------------------------------------
mainwin = Gtk.Window()
mainwin.connect("destroy",mainwin_close)
mainwin.set_border_width(10)
mainwin.set_position(Gtk.WindowPosition.CENTER)
mainwin.set_resizable(False)
mainwin.set_title(_("GDM3 Setup"))
mainwin.set_icon_name("preferences-desktop-theme")

VBox_Main = Gtk.VBox.new(False, 4)
mainwin.add(VBox_Main)

HBox_Main = Gtk.HBox.new(False, 16)
VBox_Main.pack_start(HBox_Main, False, False, 0)

VBox_Left = Gtk.VBox.new(True, 0)
HBox_Main.pack_start(VBox_Left, False, False, 0)

VBox_Right = Gtk.VBox.new(False, 0)
HBox_Main.pack_start(VBox_Right, False, False, 0)

Label_gtk = Gtk.Label(_("GTK3 theme"))
Label_gtk.set_alignment(0,0.5)
VBox_Left.pack_start(Label_gtk, False, True, 0)

ComboBox_gtk =  Gtk.ComboBoxText.new()
ComboBox_gtk.connect("changed",gtk3_theme_changed)
VBox_Right.pack_start(ComboBox_gtk, False, True, 0)

Label_bkg = Gtk.Label(_("Wallpaper"))
Label_bkg.set_alignment(0,0.5)
VBox_Left.pack_start(Label_bkg, False, True, 0)

gettext.install("gtk30")
FCB_bkg = Gtk.FileChooserButton.new(_('Select a File'),Gtk.FileChooserAction.OPEN)
FCB_bkg.set_current_folder('/usr/share/backgrounds/gnome/')
filter_bkg = Gtk.FileFilter()
filter_bkg.add_pixbuf_formats()
filter_bkg.set_name('All images')
FCB_bkg.add_filter(filter_bkg)
FCB_bkg.connect("file-set",wallpaper_changed)
VBox_Right.pack_start(FCB_bkg, False, True, 0)
gettext.install("gdm3setup")

Label_icon = Gtk.Label(_("Icon theme"))
Label_icon.set_alignment(0,0.5)
VBox_Left.pack_start(Label_icon, False, True, 0)

ComboBox_icon =  Gtk.ComboBoxText.new()
ComboBox_icon.connect("changed",icon_theme_changed)
VBox_Right.pack_start(ComboBox_icon, False, True, 0)

Label_cursor = Gtk.Label(_("Cursor theme"))
Label_cursor.set_alignment(0,0.5)
VBox_Left.pack_start(Label_cursor, False, True, 0)

ComboBox_cursor =  Gtk.ComboBoxText.new()
ComboBox_cursor.connect("changed",cursor_theme_changed)
VBox_Right.pack_start(ComboBox_cursor, False, True, 0)

Label_logo = Gtk.Label(_("Logo Icon"))
Label_logo.set_alignment(0,0.5)
VBox_Left.pack_start(Label_logo, False, True, 0)

Entry_logo =  Gtk.Entry()
Entry_logo.connect("changed",logo_icon_changed)
VBox_Right.pack_start(Entry_logo, False, True, 0)

CheckButton_banner = Gtk.CheckButton(label=_("Enable Banner"),use_underline=True)
CheckButton_banner.connect("toggled",banner_toggled)
VBox_Left.pack_start(CheckButton_banner, False, True, 0)

Entry_banner_text =  Gtk.Entry()
Entry_banner_text.set_sensitive(False)
Entry_banner_text.set_text("Wellcome")
Entry_banner_text.connect("changed",banner_text_changed)
VBox_Right.pack_start(Entry_banner_text, False, True, 0)

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

HBox9 = Gtk.HBox.new(False, 8)
VBox_Main.pack_end(HBox9, False, False, 0)

BTN_autologin = Gtk.Button(_('AutoLogin'))
BTN_autologin.connect("clicked",autologin_clicked)
HBox9.pack_start(BTN_autologin, False, False, 0)

BTN_apply = Gtk.Button(_('Apply'))
BTN_apply.connect("clicked",set_gdm)
BTN_apply.set_sensitive(False)
HBox9.pack_end(BTN_apply, False, False, 0)

BTN_Load = Gtk.Button(_('Load'))
BTN_Load.connect("clicked",get_gdm)
HBox9.pack_end(BTN_Load, False, False, 0)

#-------
win_autologin = Gtk.Window()
win_autologin.connect("delete-event",Close_AutoLogin)
win_autologin.set_border_width(10)
win_autologin.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
win_autologin.set_modal(True)
win_autologin.set_transient_for(mainwin)
win_autologin.set_resizable(False)
win_autologin.set_title(_("GDM AutoLogin Setup"))

VBoxMain_Autologin = Gtk.VBox.new(False, 8)
win_autologin.add(VBoxMain_Autologin)

CheckButton_AutoLogin = Gtk.CheckButton(label=_("Enable Automatic Login"),use_underline=True)
CheckButton_AutoLogin.connect("toggled",AutoLogin_toggled)
VBoxMain_Autologin.pack_start(CheckButton_AutoLogin, False, False, 0)

HBox_username = Gtk.HBox.new(False, 0)
HBox_username.set_sensitive(False)
VBoxMain_Autologin.pack_start(HBox_username, False, False, 0)

Label_username = Gtk.Label(_("User Name"))
Label_username.set_alignment(0,0.5)
HBox_username.pack_start(Label_username, False, False, 0)

Entry_username =  Gtk.Entry()
Entry_username.connect("changed",username_changed)
HBox_username.pack_end(Entry_username, False, False, 0)

HBox_Delay = Gtk.HBox.new(False, 8)
HBox_Delay.set_sensitive(False)
VBoxMain_Autologin.pack_start(HBox_Delay, False, False, 0)

CheckButton_Delay = Gtk.CheckButton(label=_("Enable Delay before autologin"),use_underline=True)
CheckButton_Delay.connect("toggled",Delay_toggled)
HBox_Delay.pack_start(CheckButton_Delay, False, False, 0)

SpinButton_Delay = Gtk.SpinButton.new_with_range(1,60,1)
SpinButton_Delay.set_value(10)
SpinButton_Delay.set_sensitive(False)
HBox_Delay.pack_end(SpinButton_Delay, False, False, 0)

HBox_AutoLogin_Apply = Gtk.HBox.new(False, 0)
VBoxMain_Autologin.pack_end(HBox_AutoLogin_Apply, False, False, 0)

BTN_AutoLogin_Apply = Gtk.Button(_('Apply'))
BTN_AutoLogin_Apply.connect("clicked",AutoLogin_Apply_clicked)
HBox_AutoLogin_Apply.pack_start(BTN_AutoLogin_Apply, True, False, 0)



mainwin.show_all()

load_gtk3_list()
load_icon_list()

Gtk.main()

#! /usr/bin/python2
# -*- coding: utf-8 -*-

import os
import gettext
import dbus

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GnomeDesktop
from gi.repository import GObject
from gi.repository import Gio

gettext.install("gdm3setup")

GTK3_THEME = u"Zukitwo"
SHELL_THEME = u"Adwaita"
ICON_THEME = u"Faenza-Dark"
FONT_NAME = u"Cantarell 11"
CURSOR_THEME = u"Adwaita"
WALLPAPER = u"/usr/share/backgrounds/gnome/Terraform-blue.jpg"
LOGO_ICON = u"distributor-logo"
USER_LIST = False
MENU_BTN = False
BANNER = False
BANNER_TEXT = u"Welcome"

#-----------------------------------------------
class WallpaperChooserClass(Gtk.HBox):

	def __init__(self):
		Gtk.HBox.__init__(self)
		gettext.install("gtk30")
		self.Button = Gtk.Button(_('(None)'))
		self.add(self.Button)
		gettext.install("gdm3setup")
		self.Label = self.Button.get_children()[0]
		self.Image = Gtk.Image()
		self.Image.set_from_icon_name("fileopen",Gtk.IconSize.SMALL_TOOLBAR)
		self.Sepparator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
		self.Box = Gtk.HBox.new(False,0)
		self.Button.remove(self.Label)
		self.Button.add(self.Box)
		self.Box.pack_start(self.Label,False,False,2)
		self.Box.pack_end(self.Image,False,False,2)
		self.Box.pack_end(self.Sepparator,False,False,2)
		GObject.signal_new("file-changed", WallpaperChooserClass, GObject.SIGNAL_RUN_FIRST,GObject.TYPE_NONE, ())
		self.Filename = ""
		self.Button.connect("clicked",self._Clicked)

	def Get_Filename(self):
		return self.Filename

	def Set_Filename(self,filename=""):
		self.Filename = filename
		self.Label.set_label(os.path.basename(filename))
		self.emit("file-changed")

	def _Clicked(self,e) :
		gettext.install("gtk30")
		self.FileChooserDialog = Gtk.FileChooserDialog(title=_("Select a File"),action=Gtk.FileChooserAction.OPEN,buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.ACCEPT))
		gettext.install("gdm3setup")
		filter = Gtk.FileFilter()
		filter.add_pixbuf_formats()
		filter.set_name('Image')
		self.PreviewImage = Gtk.Image()
		self.PreviewBox = Gtk.VBox.new(False, 16)
		self.PreviewBox.set_size_request(200,-1);
		self.PreviewBox.pack_start(self.PreviewImage, False, False, 0)
		self.PreviewImage.show()
		self.FileChooserDialog.add_filter(filter)
		self.FileChooserDialog.set_filename(self.Filename)
		self.FileChooserDialog.add_shortcut_folder('/usr/share/backgrounds')
		self.FileChooserDialog.set_preview_widget(self.PreviewBox)
		self.FileChooserDialog.set_preview_widget_active(False)
		self.FileChooserDialog.connect("update-preview",self._UpdatePreview)
		result = self.FileChooserDialog.run()
		if result==Gtk.ResponseType.ACCEPT :
			self.Filename = self.FileChooserDialog.get_filename()
			self.Label.set_label(os.path.basename(self.Filename))
			self.FileChooserDialog.destroy()
			self.emit("file-changed")
		else:
			self.FileChooserDialog.destroy()

	def _UpdatePreview(self,e) :
		uri = self.FileChooserDialog.get_preview_uri()
		try:
			file = Gio.File.new_for_uri(uri)
			file_info = file.query_info("*",Gio.FileQueryInfoFlags.NONE,None)
			mtime = file_info.get_attribute_uint64(Gio.FILE_ATTRIBUTE_TIME_MODIFIED)
			ThumbnailFactory = GnomeDesktop.DesktopThumbnailFactory.new(GnomeDesktop.DesktopThumbnailSize.NORMAL)
			thumbpath = ThumbnailFactory.lookup(uri,mtime)
			pixbuf = GdkPixbuf.Pixbuf.new_from_file(thumbpath)
			self.PreviewImage.set_from_pixbuf(pixbuf)
			self.FileChooserDialog.set_preview_widget_active(True)
		except Exception, e:
			self.FileChooserDialog.set_preview_widget_active(False)
			print(e)

#-----------------------------------------------
def mainwin_close(event):
	try :
		StopDaemon()
	except dbus.exceptions.DBusException :
		print ""
	Gtk.main_quit()

def load_gtk3_list():

	lst_gtk_themes = os.listdir('/usr/share/themes')

	for i in range(len(lst_gtk_themes)):
		if os.path.isdir('/usr/share/themes/'+lst_gtk_themes[i]+'/gtk-3.0') :
			ComboBox_gtk.append_text(lst_gtk_themes[i])

def load_shell_list():

	lst_shell_themes = os.listdir('/usr/share/themes')
	if not os.path.islink('/usr/share/gnome-shell/theme'):
		ComboBox_shell.append_text("Adwaita")

	for i in range(len(lst_shell_themes)):
		if os.path.isdir('/usr/share/themes/'+lst_shell_themes[i]+'/gnome-shell') :
			if os.path.isfile('/usr/share/themes/'+lst_shell_themes[i]+'/gnome-shell/gdm.css') :
				ComboBox_shell.append_text(lst_shell_themes[i])

def load_icon_list():
	lst_icons = os.listdir('/usr/share/icons')

	for i in range(len(lst_icons)):
		if os.path.isdir('/usr/share/icons/'+lst_icons[i]+'/') :
			if 	os.path.isdir('/usr/share/icons/'+lst_icons[i]+'/cursors/') :
				ComboBox_cursor.append_text(lst_icons[i])
			else :
				ComboBox_icon.append_text(lst_icons[i])

def get_setting(name,data):
	for line in data:
		line = unicode(line)
		if line[0:len(name)+1]==name+"=":
			value = line[len(name)+1:len(line)].strip()
			break
	return value

def unquote(value):
	if value[0:1] == "'"  and value[len(value)-1:len(value)] == "'" :
		value = value[1:len(value)-1]
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

def set_gdm(name,value):
	if SetUI(name,value)=="OK" :
		return True
	else :
		return False

def get_gdm():
	settings = list(GetUI())
	global GTK3_THEME,SHELL_THEME,ICON_THEME,CURSOR_THEME,WALLPAPER,LOGO_ICON,USER_LIST,MENU_BTN,BANNER,BANNER_TEXT,FONT_NAME
	GTK3_THEME = get_setting("GTK",settings)
	SHELL_THEME = get_setting("SHELL",settings)
	ICON_THEME = get_setting("ICON",settings)
	CURSOR_THEME = get_setting("CURSOR",settings)
	BKG = get_setting("BKG",settings)
	WALLPAPER = BKG[8:len(BKG)-1]
	LOGO_ICON = get_setting("LOGO",settings)
	USER_LIST = str_to_bool(get_setting("USER_LIST",settings))
	MENU_BTN = str_to_bool( get_setting("BTN" ,settings))
	BANNER = str_to_bool(get_setting("BANNER",settings))
	BANNER_TEXT = get_setting("BANNER_TEXT",settings)
	FONT_NAME = unquote(get_setting("FONT",settings))

	ComboBox_gtk.set_active_iter(get_iter(ComboBox_gtk.get_model(),GTK3_THEME))
	ComboBox_shell.set_active_iter(get_iter(ComboBox_shell.get_model(),SHELL_THEME))
	WallpaperChooser.Set_Filename(WALLPAPER) 
	ComboBox_icon.set_active_iter(get_iter(ComboBox_icon.get_model(),ICON_THEME))
	ComboBox_cursor.set_active_iter(get_iter(ComboBox_cursor.get_model(),CURSOR_THEME))
	Entry_logo.set_text(LOGO_ICON)
	CheckButton_banner.set_active(BANNER)
	Entry_banner_text.set_text(BANNER_TEXT)
	CheckButton_user.set_active(USER_LIST)
	CheckButton_restart.set_active(MENU_BTN)
	Entry_banner_text.set_sensitive(BANNER)
	FontButton.set_font_name(FONT_NAME)

def gtk3_theme_changed(e):
	global GTK3_THEME
	gtk_theme = unicode(ComboBox_gtk.get_active_text(),'UTF_8')
	if gtk_theme!=unquote(GTK3_THEME) :
		if set_gdm('GTK_THEME',gtk_theme) :
			GTK3_THEME = gtk_theme
			print("GTK3 Theme Changed : " + GTK3_THEME)
		else :
			ComboBox_gtk.set_active_iter(get_iter(ComboBox_gtk.get_model(),GTK3_THEME))

def shell_theme_changed(e):
	global SHELL_THEME
	shell_theme = unicode(ComboBox_shell.get_active_text(),'UTF_8')
	if shell_theme!=unquote(SHELL_THEME) :
		if set_gdm('SHELL_THEME',shell_theme) :
			SHELL_THEME = shell_theme
			print("SHELL Theme Changed : " + SHELL_THEME)
		else :
			ComboBox_shell.set_active_iter(get_iter(ComboBox_shell.get_model(),SHELL_THEME))

def font_set(e):
	global FONT_NAME
	font_name = FontButton.get_font_name()
	if FONT_NAME != font_name : 
		if set_gdm('FONT',font_name) :
			FONT_NAME = font_name
			print("Font Changed : " + font_name)
		else :
			FontButton.set_font_name(FONT_NAME)

def wallpaper_filechanged(e):
	global WALLPAPER
	wallpaper = WallpaperChooser.Get_Filename()
	if WALLPAPER != wallpaper :
		if set_gdm('WALLPAPER',wallpaper) :
			WALLPAPER = wallpaper 
			print("Wallpaper Changed : " + WALLPAPER)
		else :
			WallpaperChooser.Set_Filename(WALLPAPER)

def icon_theme_changed(e):
	global ICON_THEME
	icon_theme = unicode(ComboBox_icon.get_active_text(),'UTF_8')
	if unquote(ICON_THEME) != icon_theme:
		if set_gdm('ICON_THEME',icon_theme) :
			ICON_THEME = icon_theme
			print ("Icon Theme Changed : " + ICON_THEME)
		else:
			ComboBox_icon.set_active_iter(get_iter(ComboBox_icon.get_model(),ICON_THEME))

def cursor_theme_changed(e):
	global CURSOR_THEME
	cursor_theme = unicode(ComboBox_cursor.get_active_text(),'UTF_8')
	if unquote(CURSOR_THEME) != cursor_theme:
		if set_gdm('CURSOR_THEME',cursor_theme) :
			CURSOR_THEME = cursor_theme
			print ("Cursor Theme Changed : " + CURSOR_THEME)
		else :
			ComboBox_cursor.set_active_iter(get_iter(ComboBox_cursor.get_model(),CURSOR_THEME))

def logo_icon_changed(e):
	global LOGO_ICON
	logo_icon = unicode(Entry_logo.get_text(),'UTF_8')
	if LOGO_ICON != logo_icon :
		if set_gdm('LOGO_ICON',logo_icon) :
			LOGO_ICON = logo_icon
			print ("Logo Icon Changed : " + LOGO_ICON)
		else:
			Entry_logo.set_text(LOGO_ICON)

def banner_toggled(e):
	global BANNER
	banner = CheckButton_banner.get_active()
	if banner!=BANNER :
		if set_gdm('BANNER',str(banner)) :
			BANNER = banner
			print ("Banner Changed : " + str(BANNER))

			if BANNER :
				Entry_banner_text.set_sensitive(True)
			else:
				Entry_banner_text.set_sensitive(False)
		else:
			CheckButton_banner.set_active(BANNER)

def banner_text_changed(e):
	global BANNER_TEXT
	banner_text = unicode(Entry_banner_text.get_text(),'UTF_8')
	if banner_text!=BANNER_TEXT :
		if set_gdm('BANNER_TEXT',banner_text) :
			BANNER_TEXT = banner_text
			print ("Banner Text Changed : " + BANNER_TEXT)
		else :
			Entry_banner_text.set_text(BANNER_TEXT)

def user_list_toggled(e):
	global USER_LIST
	user_list = CheckButton_user.get_active()
	if USER_LIST != user_list :
		if set_gdm('USER_LIST',str(user_list)) :
			USER_LIST = user_list
			print ("User List Changed : " + str(USER_LIST))
		else:
			CheckButton_user.set_active(USER_LIST)

def menu_btn_toggled(e):
	global MENU_BTN
	menu_btn = CheckButton_restart.get_active()
	if MENU_BTN != menu_btn :
		if set_gdm('MENU_BTN',str(menu_btn)) :
			MENU_BTN = menu_btn
			print ("Menu Btn Changed : " + str(MENU_BTN))
		else:
			CheckButton_restart.set_active(MENU_BTN)


#--------------------------------------------------------

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

	SetAutoLogin(AUTOLOGIN,USERNAME,TIMED,int(TIMED_TIME))

	win_autologin.hide()

def get_autologin():
	AUTOLOGIN,USERNAME,TIMED,TIMED_TIME = GetAutoLogin()
	CheckButton_AutoLogin.set_active(str_to_bool(AUTOLOGIN))
	CheckButton_Delay.set_active(str_to_bool(TIMED))
	SpinButton_Delay.set_value(int(TIMED_TIME))
	Entry_username.set_text(USERNAME)

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
VBox_Right.pack_start(ComboBox_gtk, False, True, 0)

Label_shell = Gtk.Label(_("Shell theme"))
Label_shell.set_alignment(0,0.5)
VBox_Left.pack_start(Label_shell, False, True, 0)

ComboBox_shell =  Gtk.ComboBoxText.new()
VBox_Right.pack_start(ComboBox_shell, False, True, 0)

Label_bkg = Gtk.Label(_("Wallpaper"))
Label_bkg.set_alignment(0,0.5)
VBox_Left.pack_start(Label_bkg, False, True, 0)

WallpaperChooser = WallpaperChooserClass()
VBox_Right.pack_start(WallpaperChooser, False, True, 0)

Label_font = Gtk.Label(_("Font"))
Label_font.set_alignment(0,0.5)
VBox_Left.pack_start(Label_font, False, True, 0)

FontButton = Gtk.FontButton.new()
VBox_Right.pack_start(FontButton, False, True, 0)

Label_icon = Gtk.Label(_("Icon theme"))
Label_icon.set_alignment(0,0.5)
VBox_Left.pack_start(Label_icon, False, True, 0)

ComboBox_icon =  Gtk.ComboBoxText.new()
VBox_Right.pack_start(ComboBox_icon, False, True, 0)

Label_cursor = Gtk.Label(_("Cursor theme"))
Label_cursor.set_alignment(0,0.5)
VBox_Left.pack_start(Label_cursor, False, True, 0)

ComboBox_cursor =  Gtk.ComboBoxText.new()
VBox_Right.pack_start(ComboBox_cursor, False, True, 0)

Label_logo = Gtk.Label(_("Logo Icon"))
Label_logo.set_alignment(0,0.5)
VBox_Left.pack_start(Label_logo, False, True, 0)

Entry_logo = Gtk.Entry()
VBox_Right.pack_start(Entry_logo, False, True, 0)

CheckButton_banner = Gtk.CheckButton(label=_("Enable Banner"),use_underline=True)
VBox_Left.pack_start(CheckButton_banner, False, True, 0)

Entry_banner_text = Gtk.Entry()
Entry_banner_text.set_sensitive(False)
VBox_Right.pack_start(Entry_banner_text, False, True, 0)

HBox_user = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_user, False, True, 0)

CheckButton_user = Gtk.CheckButton(label=_("Disable User List"),use_underline=True)
HBox_user.pack_start(CheckButton_user, False, True, 0)

HBox_restart = Gtk.HBox.new(True, 0)
VBox_Main.pack_start(HBox_restart, False, True, 0)

CheckButton_restart = Gtk.CheckButton(label=_("Disable Restart Buttons"),use_underline=True)
HBox_restart.pack_start(CheckButton_restart, False, True, 0)

HBox_autologin = Gtk.HBox.new(False, 8)
VBox_Main.pack_end(HBox_autologin, False, False, 0)

BTN_autologin = Gtk.Button(_('AutoLogin'))
BTN_autologin.connect("clicked",autologin_clicked)
HBox_autologin.pack_start(BTN_autologin, False, False, 0)

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

bus = dbus.SystemBus()
gdm3setup = bus.get_object('apps.nano77.gdm3setup','/apps/nano77/gdm3setup')
SetUI = gdm3setup.get_dbus_method('SetUI','apps.nano77.gdm3setup')
GetUI = gdm3setup.get_dbus_method('GetUI','apps.nano77.gdm3setup')
SetAutoLogin = gdm3setup.get_dbus_method('SetAutoLogin','apps.nano77.gdm3setup')
GetAutoLogin = gdm3setup.get_dbus_method('GetAutoLogin','apps.nano77.gdm3setup')
StopDaemon = gdm3setup.get_dbus_method('StopDaemon', 'apps.nano77.gdm3setup')

load_gtk3_list()
load_shell_list()
load_icon_list()
get_gdm()
get_autologin()

FontButton.connect("font-set",font_set)
WallpaperChooser.connect("file-changed",wallpaper_filechanged)
ComboBox_shell.connect("changed",shell_theme_changed)
ComboBox_icon.connect("changed",icon_theme_changed)
ComboBox_cursor.connect("changed",cursor_theme_changed)
Entry_logo.connect("changed",logo_icon_changed)
ComboBox_gtk.connect("changed",gtk3_theme_changed)
CheckButton_banner.connect("toggled",banner_toggled)
Entry_banner_text.connect("changed",banner_text_changed)
CheckButton_user.connect("toggled",user_list_toggled)
CheckButton_restart.connect("toggled",menu_btn_toggled)


Gtk.main()

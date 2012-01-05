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
from gi.repository import GLib

gettext.install("gdm3setup")

#-----------------------------------------------
class WallpaperChooserButton(Gtk.Button):

	def __init__(self):
		Gtk.Button.__init__(self)
		self.Label = Gtk.Label(_('(None)'))
		self.Image = Gtk.Image()
		self.Image.set_from_icon_name("fileopen",Gtk.IconSize.SMALL_TOOLBAR)
		self.Separator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
		self.Box = Gtk.HBox.new(False,0)
		self.add(self.Box)
		self.Box.pack_start(self.Label,False,False,2)
		self.Box.pack_end(self.Image,False,False,2)
		self.Box.pack_end(self.Separator,False,False,2)
		self.PreviewImage = Gtk.Image()
		self.PreviewBox = Gtk.VBox.new(False, 16)
		self.Filename = ""
		self.connect("clicked",self._Clicked)

	def get_filename(self):
		return self.Filename

	def set_filename(self,filename=""):
		self.Filename = filename
		if filename != "" :
			self.Label.set_label(os.path.basename(filename))
		else :
			self.Label.set_label(_("(None)"))
		self.emit("file-changed")

	def _Clicked(self,e) :
		self.FileChooserDialog = Gtk.FileChooserDialog(title=_("Select a File"),action=Gtk.FileChooserAction.OPEN,buttons=(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_CLEAR,Gtk.ResponseType.NONE,Gtk.STOCK_OPEN,Gtk.ResponseType.ACCEPT))
		filter = Gtk.FileFilter()
		filter.add_pixbuf_formats()
		filter.set_name('Image')
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
		elif result==Gtk.ResponseType.NONE :
			self.Filename = ""
			self.Label.set_label(_("(None)"))
			self.FileChooserDialog.destroy()
			self.emit("file-changed")
		else:
			self.FileChooserDialog.destroy()

	def _UpdatePreview(self,e) :
		uri = self.FileChooserDialog.get_preview_uri()
		if uri!=None :
			if not GLib.file_test(GLib.filename_from_uri(uri,""),GLib.FileTest.IS_DIR) :
				file = Gio.File.new_for_uri(uri)
				file_info = file.query_info("*",Gio.FileQueryInfoFlags.NONE,None)
				mtime = file_info.get_attribute_uint64(Gio.FILE_ATTRIBUTE_TIME_MODIFIED)
				ThumbnailFactory = GnomeDesktop.DesktopThumbnailFactory.new(GnomeDesktop.DesktopThumbnailSize.NORMAL)
				thumbpath = ThumbnailFactory.lookup(uri,mtime)
				pixbuf = GdkPixbuf.Pixbuf.new_from_file(thumbpath)
				self.PreviewImage.set_from_pixbuf(pixbuf)
				self.FileChooserDialog.set_preview_widget_active(True)
			else :
				self.FileChooserDialog.set_preview_widget_active(False)
		else :
			self.FileChooserDialog.set_preview_widget_active(False)

GObject.signal_new("file-changed", WallpaperChooserButton, GObject.SIGNAL_RUN_FIRST,GObject.TYPE_NONE, ())


class AutologinButton (Gtk.Button) :
	def __init__(self,parent_window):
		Gtk.Button.__init__(self)
		self.autologin=False
		self.username=""
		self.timed=False
		self.time=30
		self.box=Gtk.HBox(False,0)
		self.add(self.box)
		self.label_state=Gtk.Label(_("Disabled"))
		self.label_state.set_no_show_all(True)
		self.label_state.show()
		self.box.pack_start(self.label_state,True,True,2)
		self.label_user=Gtk.Label("USER")
		self.label_user.set_no_show_all(True)
		self.box.pack_start(self.label_user,False,False,2)
		self.label_time=Gtk.Label("TIME")
		self.label_time.set_no_show_all(True)
		self.box.pack_end(self.label_time,False,False,2)
		self.Separator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
		self.Separator.set_no_show_all(True)
		self.box.pack_end(self.Separator,False,False,2)
		self.connect("clicked",self._clicked)
		self.window = AutoLoginWindow(parent_window)
		self.window.connect("changed",self._changed)

		GObject.signal_new("changed", AutologinButton, GObject.SIGNAL_RUN_FIRST,GObject.TYPE_NONE, ())

	def update(self) :
		if self.autologin :
			self.label_state.hide()
			self.label_user.show()
			if self.timed :
				self.Separator.show()
				self.label_time.show()
			else :
				self.Separator.hide()
				self.label_time.hide()
		else :
			self.label_state.show()
			self.label_user.hide()
			self.Separator.hide()
			self.label_time.hide()
		self.label_user.set_text(self.username)
		self.label_time.set_text(str(self.time) + " s")

	def set_autologin(self,b) :
		self.autologin = b
		self.update()

	def get_autologin(self) :
		return self.autologin

	def set_timed(self,timed):
		self.timed=timed
		self.update()

	def get_timed(self):
		return self.timed

	def set_time(self,time):
		self.time=time
		self.update()

	def get_time(self):
		return self.time

	def set_username(self,username):
		self.username=username
		self.update()

	def get_username(self):
		return self.username

	def _clicked(self,e) :
		self.window.CheckButton_AutoLogin.set_active(self.get_autologin())
		self.window.Entry_username.set_text(self.get_username())
		self.window.CheckButton_Delay.set_active(self.get_timed())
		self.window.SpinButton_Delay.set_value(self.get_time())
		self.window.show_all()

	def _changed(self,e) :
		self.set_autologin(self.window.CheckButton_AutoLogin.get_active())
		self.set_username(self.window.Entry_username.get_text())
		self.set_timed(self.window.CheckButton_Delay.get_active())
		self.set_time(self.window.SpinButton_Delay.get_value_as_int())

		self.emit("changed")


class AutoLoginWindow(Gtk.Window):
	def __init__(self,parent_window):
		Gtk.Window.__init__(self)
		self.connect("delete-event",self._Close)
		self.set_border_width(10)
		self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
		self.set_modal(True)
		self.set_transient_for(parent_window)
		self.set_resizable(False)
		self.set_title(_("GDM AutoLogin Setup"))

		self.VBoxMain = Gtk.VBox.new(False, 8)
		self.add(self.VBoxMain)

		self.CheckButton_AutoLogin = Gtk.CheckButton(label=_("Enable Automatic Login"),use_underline=True)
		self.CheckButton_AutoLogin.connect("toggled",self.AutoLogin_toggled)
		self.VBoxMain.pack_start(self.CheckButton_AutoLogin, False, False, 0)

		self.HBox_username = Gtk.HBox.new(False, 0)
		self.HBox_username.set_sensitive(False)
		self.VBoxMain.pack_start(self.HBox_username, False, False, 0)

		self.Label_username = Gtk.Label(_("User Name"))
		self.Label_username.set_alignment(0,0.5)
		self.HBox_username.pack_start(self.Label_username, False, False, 0)

		self.Entry_username =  Gtk.Entry()
		self.Entry_username.connect("changed",self.username_changed)
		self.HBox_username.pack_end(self.Entry_username, False, False, 0)

		self.HBox_Delay = Gtk.HBox.new(False, 8)
		self.HBox_Delay.set_sensitive(False)
		self.VBoxMain.pack_start(self.HBox_Delay, False, False, 0)

		self.CheckButton_Delay = Gtk.CheckButton(label=_("Enable Delay before autologin"),use_underline=True)
		self.CheckButton_Delay.connect("toggled",self.Delay_toggled)
		self.HBox_Delay.pack_start(self.CheckButton_Delay, False, False, 0)

		self.SpinButton_Delay = Gtk.SpinButton.new_with_range(1,60,1)
		self.SpinButton_Delay.set_value(10)
		self.SpinButton_Delay.set_sensitive(False)
		self.HBox_Delay.pack_end(self.SpinButton_Delay, False, False, 0)

		self.HBox_Apply = Gtk.HBox.new(False, 0)
		self.VBoxMain.pack_end(self.HBox_Apply, False, False, 0)

		self.BTN_Apply = Gtk.Button(_('Apply'))
		self.BTN_Apply.connect("clicked",self.Apply_clicked)
		self.HBox_Apply.pack_start(self.BTN_Apply, True, False, 0)


	def _Close(self,e,data):
		self.hide()
		return True

	def AutoLogin_toggled(self,e):
		if self.CheckButton_AutoLogin.get_active():
			self.HBox_username.set_sensitive(True)
			self.HBox_Delay.set_sensitive(True)
		else:
			self.HBox_username.set_sensitive(False)
			self.HBox_Delay.set_sensitive(False)

		if self.Entry_username.get_text()!="" or not self.CheckButton_AutoLogin.get_active():
			self.HBox_Apply.set_sensitive(True)
		else:
			self.HBox_Apply.set_sensitive(False)

	def username_changed(self,e):
		if self.Entry_username.get_text()!="":
			self.HBox_Apply.set_sensitive(True)
		else:
			self.HBox_Apply.set_sensitive(False)

	def Delay_toggled(self,e):
		if self.CheckButton_Delay.get_active():
			self.SpinButton_Delay.set_sensitive(True)
		else:
			self.SpinButton_Delay.set_sensitive(False)

	def Apply_clicked(self,e):
		self.emit("changed")
		self.hide()

GObject.signal_new("changed", AutoLoginWindow, GObject.SIGNAL_RUN_FIRST,GObject.TYPE_NONE, ())


class MainWindow(Gtk.Window) :
	def __init__(self) :
		Gtk.Window.__init__(self)
		self.connect("destroy",self._close)
		self.set_border_width(10)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.set_resizable(False)
		self.set_title(_("GDM3 Setup"))
		self.set_icon_name("preferences-desktop-theme")

		self.VBox_Main = Gtk.VBox.new(False, 0)
		self.add(self.VBox_Main)
		self.notebook = Gtk.Notebook()
		self.VBox_Main.pack_start(self.notebook, False, False, 0)

		self.Box_common = Gtk.VBox.new(False, 0)
		self.Box_common.set_border_width(10)
		self.common_label = Gtk.Label(_("General"))
		self.notebook.append_page(self.Box_common,self.common_label)
		self.Box_common_main = Gtk.HBox.new(False, 10)
		self.Box_common.pack_start(self.Box_common_main, False, False, 0)
		self.Box_common_Left = Gtk.VBox.new(True, 0)
		self.Box_common_main.pack_start(self.Box_common_Left, False, False, 0)
		self.Box_common_Right = Gtk.VBox.new(True, 0)
		self.Box_common_main.pack_end(self.Box_common_Right, False, False, 0)

		self.Box_shell = Gtk.VBox.new(False, 0)
		self.Box_shell.set_border_width(10)
		self.shell_label = Gtk.Label("GnomeShell")
		self.notebook.append_page(self.Box_shell,self.shell_label)
		self.Box_shell_main = Gtk.HBox.new(False, 0)
		self.Box_shell.pack_start(self.Box_shell_main, False, False, 0)
		self.Box_shell_Left = Gtk.VBox.new(True, 0)
		self.Box_shell_main.pack_start(self.Box_shell_Left, False, False, 0)
		self.Box_shell_Right = Gtk.VBox.new(True, 0)
		self.Box_shell_main.pack_end(self.Box_shell_Right, False, False, 0)
		self.Box_shell_date = Gtk.HBox.new(False, 0)
		self.Box_shell.pack_start(self.Box_shell_date, False, False, 5)
		self.Box_shell_seconds = Gtk.HBox.new(False, 0)
		self.Box_shell.pack_start(self.Box_shell_seconds, False, False, 5)

		self.Box_gtk = Gtk.VBox.new(False, 0)
		self.Box_gtk.set_border_width(10)
		self.gtk_label = Gtk.Label("GTK")
		self.notebook.append_page(self.Box_gtk,self.gtk_label)
		self.Box_gtk_main = Gtk.HBox.new(False, 0)
		self.Box_gtk.pack_start(self.Box_gtk_main, False, False, 0)
		self.Box_gtk_Left = Gtk.VBox.new(True, 0)
		self.Box_gtk_main.pack_start(self.Box_gtk_Left, False, False, 0)
		self.Box_gtk_Right = Gtk.VBox.new(True, 0)
		self.Box_gtk_main.pack_end(self.Box_gtk_Right, False, False, 0)

		self.Label_bkg = Gtk.Label(_("Wallpaper"))
		self.Label_bkg.set_alignment(0,0.5)
		self.Box_common_Left.pack_start(self.Label_bkg, False, False, 0)
		self.WallpaperChooser = WallpaperChooserButton()
		self.Box_common_Right.pack_start(self.WallpaperChooser, False, False, 0)
		self.Label_icon = Gtk.Label(_("Icon theme"))
		self.Label_icon.set_alignment(0,0.5)
		self.Box_common_Left.pack_start(self.Label_icon, False, False, 0)
		self.ComboBox_icon =  Gtk.ComboBoxText.new()
		self.Box_common_Right.pack_start(self.ComboBox_icon, False, False, 0)
		self.Label_cursor = Gtk.Label(_("Cursor theme"))
		self.Label_cursor.set_alignment(0,0.5)
		self.Box_common_Left.pack_start(self.Label_cursor, False, False, 0)
		self.ComboBox_cursor =  Gtk.ComboBoxText.new()
		self.Box_common_Right.pack_start(self.ComboBox_cursor, False, False, 0)
		self.Label_Autologin = Gtk.Label(_("AutoLogin"))
		self.Label_Autologin.set_alignment(0,0.5)
		self.Box_common_Left.pack_start(self.Label_Autologin, False, False, 0)
		self.BTN_autologin = AutologinButton(self)
		self.Box_common_Right.pack_start(self.BTN_autologin, False, False, 0)

		self.Label_shell = Gtk.Label(_("Shell theme"))
		self.Label_shell.set_alignment(0,0.5)
		self.Box_shell_Left.pack_start(self.Label_shell, False, False, 0)
		self.ComboBox_shell = Gtk.ComboBoxText.new()
		self.Box_shell_Right.pack_start(self.ComboBox_shell, False, False, 0)
		self.Label_shell_logo = Gtk.Label(_("Shell Logo"))
		self.Label_shell_logo.set_alignment(0,0.5)
		self.Box_shell_Left.pack_start(self.Label_shell_logo, False, False, 0)
		self.BTN_shell_logo = WallpaperChooserButton()
		self.Box_shell_Right.pack_start(self.BTN_shell_logo, False, False, 0)
		self.Label_clock_date = Gtk.Label(_("Show Date in Clock"))
		self.Label_clock_date.set_alignment(0,0.5)
		self.Box_shell_date.pack_start(self.Label_clock_date, False, False, 0)
		self.Switch_clock_date = Gtk.Switch()
		self.Box_shell_date.pack_end(self.Switch_clock_date, False, False, 0)
		self.Label_clock_seconds = Gtk.Label(_("Show Seconds in Clock"))
		self.Label_clock_seconds.set_alignment(0,0.5)
		self.Box_shell_seconds.pack_start(self.Label_clock_seconds, False, False, 0)
		self.Switch_clock_seconds = Gtk.Switch()
		self.Box_shell_seconds.pack_end(self.Switch_clock_seconds, False, False, 0)

		self.Label_gtk = Gtk.Label(_("GTK3 theme"))
		self.Label_gtk.set_alignment(0,0.5)
		self.Box_gtk_Left.pack_start(self.Label_gtk, False, False, 0)
		self.ComboBox_gtk =  Gtk.ComboBoxText.new()
		self.Box_gtk_Right.pack_start(self.ComboBox_gtk, False, False, 0)
		self.Label_font = Gtk.Label(_("Font"))
		self.Label_font.set_alignment(0,0.5)
		self.Box_gtk_Left.pack_start(self.Label_font, False, False, 0)
		self.FontButton = Gtk.FontButton.new()
		self.Box_gtk_Right.pack_start(self.FontButton, False, False, 0)
		self.Label_logo = Gtk.Label(_("Logo Icon"))
		self.Label_logo.set_alignment(0,0.5)
		self.Box_gtk_Left.pack_start(self.Label_logo, False, False, 0)
		self.Entry_logo_icon = Gtk.Entry()
		self.Box_gtk_Right.pack_start(self.Entry_logo_icon, False, False, 0)
		self.CheckButton_banner = Gtk.CheckButton(label=_("Enable Banner"),use_underline=False)
		self.Box_gtk_Left.pack_start(self.CheckButton_banner, False, False, 0)
		self.Entry_banner_text = Gtk.Entry()
		self.Entry_banner_text.set_sensitive(False)
		self.Box_gtk_Right.pack_start(self.Entry_banner_text, False, False, 0)
		self.HBox_user = Gtk.HBox.new(False, 0)
		self.Box_gtk.pack_start(self.HBox_user, False, False, 5)
		self.CheckButton_user = Gtk.CheckButton(label=_("Disable User List"),use_underline=False)
		self.HBox_user.pack_start(self.CheckButton_user, False, False, 0)
		self.HBox_restart = Gtk.HBox.new(False, 0)
		self.Box_gtk.pack_start(self.HBox_restart, False, False, 5)
		self.CheckButton_restart = Gtk.CheckButton(label=_("Disable Restart Buttons"),use_underline=False)
		self.HBox_restart.pack_start(self.CheckButton_restart, False, False, 0)

		proxy = dbus.SystemBus().get_object('apps.nano77.gdm3setup','/apps/nano77/gdm3setup')
		self.SetUI = proxy.get_dbus_method('SetUI','apps.nano77.gdm3setup')
		self.GetUI = proxy.get_dbus_method('GetUI','apps.nano77.gdm3setup')
		self.SetAutoLogin = proxy.get_dbus_method('SetAutoLogin','apps.nano77.gdm3setup')
		self.GetAutoLogin = proxy.get_dbus_method('GetAutoLogin','apps.nano77.gdm3setup')
		self.StopDaemon = proxy.get_dbus_method('StopDaemon', 'apps.nano77.gdm3setup')

		self.load_gtk3_list()
		self.load_shell_list()
		self.load_icon_list()
		self.get_gdm()
		self.get_autologin()

		self.FontButton.connect("font-set",self.font_set)
		self.WallpaperChooser.connect("file-changed",self.wallpaper_filechanged)
		self.ComboBox_shell.connect("changed",self.shell_theme_changed)
		self.ComboBox_icon.connect("changed",self.icon_theme_changed)
		self.ComboBox_cursor.connect("changed",self.cursor_theme_changed)
		self.Entry_logo_icon.connect("changed",self.logo_icon_changed)
		self.BTN_shell_logo.connect("file-changed",self.shell_logo_changed)
		self.ComboBox_gtk.connect("changed",self.gtk3_theme_changed)
		self.CheckButton_banner.connect("toggled",self.banner_toggled)
		self.Entry_banner_text.connect("changed",self.banner_text_changed)
		self.CheckButton_user.connect("toggled",self.user_list_toggled)
		self.CheckButton_restart.connect("toggled",self.menu_btn_toggled)
		self.BTN_autologin.connect("changed",self.autologin_changed)
		self.Switch_clock_date.connect("notify::active",self.clock_date_toggled)
		self.Switch_clock_seconds.connect("notify::active",self.clock_seconds_toggled)

	def load_gtk3_list(self):
		lst_gtk_themes = os.listdir('/usr/share/themes')
		for i in range(len(lst_gtk_themes)) :
			if os.path.isdir('/usr/share/themes/'+lst_gtk_themes[i]+'/gtk-3.0') :
				self.ComboBox_gtk.append_text(lst_gtk_themes[i])

	def load_shell_list(self):

		lst_shell_themes = os.listdir('/usr/share/themes')
		if not os.path.islink('/usr/share/gnome-shell/theme'):
			self.ComboBox_shell.append_text("Adwaita")

		for i in range(len(lst_shell_themes)):
			if os.path.isdir('/usr/share/themes/'+lst_shell_themes[i]+'/gnome-shell') :
				if os.path.isfile('/usr/share/themes/'+lst_shell_themes[i]+'/gnome-shell/gdm.css') :
					self.ComboBox_shell.append_text(lst_shell_themes[i])

	def load_icon_list(self):
		lst_icons = os.listdir('/usr/share/icons')

		for i in range(len(lst_icons)):
			if os.path.isdir('/usr/share/icons/'+lst_icons[i]+'/') :
				if 	os.path.isdir('/usr/share/icons/'+lst_icons[i]+'/cursors/') :
					self.ComboBox_cursor.append_text(lst_icons[i])
				else :
					self.ComboBox_icon.append_text(lst_icons[i])

	def _close(self,e):
		try :
			self.StopDaemon()
		except dbus.exceptions.DBusException :
			print ""
		Gtk.main_quit()

	def set_gdm(self,name,value):
		if self.SetUI(name,value)=="OK" :
			return True
		else :
			return False

	def get_gdm(self):
		settings = list(self.GetUI())
		self.GTK3_THEME = get_setting("GTK",settings)
		self.SHELL_THEME = get_setting("SHELL",settings)
		self.ICON_THEME = get_setting("ICON",settings)
		self.CURSOR_THEME = get_setting("CURSOR",settings)
		BKG = get_setting("WALLPAPER",settings)
		self.WALLPAPER = BKG[8:len(BKG)-1]
		self.LOGO_ICON = get_setting("LOGO_ICON",settings)
		self.SHELL_LOGO = unquote(get_setting("SHELL_LOGO",settings))
		self.USER_LIST = str_to_bool(get_setting("USER_LIST",settings))
		self.MENU_BTN = str_to_bool( get_setting("BTN" ,settings))
		self.BANNER = str_to_bool(get_setting("BANNER",settings))
		self.BANNER_TEXT = get_setting("BANNER_TEXT",settings)
		self.FONT_NAME = unquote(get_setting("FONT",settings))
		self.CLOCK_DATE = str_to_bool(get_setting("CLOCK_DATE",settings))
		self.CLOCK_SECONDS = str_to_bool(get_setting("CLOCK_SECONDS",settings))
		self.ComboBox_gtk.set_active_iter(get_iter(self.ComboBox_gtk.get_model(),self.GTK3_THEME))
		self.ComboBox_shell.set_active_iter(get_iter(self.ComboBox_shell.get_model(),self.SHELL_THEME))
		self.WallpaperChooser.set_filename(self.WALLPAPER) 
		self.ComboBox_icon.set_active_iter(get_iter(self.ComboBox_icon.get_model(),self.ICON_THEME))
		self.ComboBox_cursor.set_active_iter(get_iter(self.ComboBox_cursor.get_model(),self.CURSOR_THEME))
		self.Entry_logo_icon.set_text(self.LOGO_ICON)
		self.BTN_shell_logo.set_filename(self.SHELL_LOGO)
		self.CheckButton_banner.set_active(self.BANNER)
		self.Entry_banner_text.set_text(self.BANNER_TEXT)
		self.CheckButton_user.set_active(self.USER_LIST)
		self.CheckButton_restart.set_active(self.MENU_BTN)
		self.Entry_banner_text.set_sensitive(self.BANNER)
		self.FontButton.set_font_name(self.FONT_NAME)
		self.Switch_clock_date.set_active(self.CLOCK_DATE)
		self.Switch_clock_seconds.set_active(self.CLOCK_SECONDS)

	def set_autologin(self,autologin,username,timed,time):
		if self.SetAutoLogin(autologin,username,timed,time)=="OK" :
			return True
		else :
			return False

	def get_autologin(self):
		AUTOLOGIN,USERNAME,TIMED,TIMED_TIME = self.GetAutoLogin()
		self.AUTOLOGIN_ENABLED = str_to_bool(AUTOLOGIN)
		self.AUTOLOGIN_USERNAME = USERNAME
		self.AUTOLOGIN_TIMED = str_to_bool(TIMED)
		self.AUTOLOGIN_TIME = int(TIMED_TIME)
		self.BTN_autologin.set_autologin(self.AUTOLOGIN_ENABLED) 
		self.BTN_autologin.set_username(self.AUTOLOGIN_USERNAME)
		self.BTN_autologin.set_timed(self.AUTOLOGIN_TIMED) 
		self.BTN_autologin.set_time(self.AUTOLOGIN_TIME)

	def gtk3_theme_changed(self,e):
		gtk_theme = unicode(self.ComboBox_gtk.get_active_text(),'UTF_8')
		if gtk_theme!=unquote(self.GTK3_THEME) :
			if self.set_gdm('GTK_THEME',gtk_theme) :
				self.GTK3_THEME = gtk_theme
				print("GTK3 Theme Changed : " + self.GTK3_THEME)
			else :
				self.ComboBox_gtk.set_active_iter(get_iter(self.ComboBox_gtk.get_model(),self.GTK3_THEME))

	def shell_theme_changed(self,e):
		shell_theme = unicode(self.ComboBox_shell.get_active_text(),'UTF_8')
		if shell_theme!=unquote(self.SHELL_THEME) :
			if self.set_gdm('SHELL_THEME',shell_theme) :
				self.SHELL_THEME = shell_theme
				print("SHELL Theme Changed : " + self.SHELL_THEME)
			else :
				self.ComboBox_shell.set_active_iter(get_iter(self.ComboBox_shell.get_model(),self.SHELL_THEME))

	def font_set(self,e):
		font_name = self.FontButton.get_font_name()
		if self.FONT_NAME != font_name : 
			if self.set_gdm('FONT',font_name) :
				self.FONT_NAME = font_name
				print("Font Changed : " + self.FONT_NAME)
			else :
				self.FontButton.set_font_name(self.FONT_NAME)

	def wallpaper_filechanged(self,e):
		wallpaper = self.WallpaperChooser.get_filename()
		if self.WALLPAPER != wallpaper :
			if self.set_gdm('WALLPAPER',wallpaper) :
				self.WALLPAPER = wallpaper 
				print("Wallpaper Changed : " + self.WALLPAPER)
			else :
				self.WallpaperChooser.set_filename(self.WALLPAPER)

	def icon_theme_changed(self,e):
		icon_theme = unicode(self.ComboBox_icon.get_active_text(),'UTF_8')
		if unquote(self.ICON_THEME) != icon_theme:
			if self.set_gdm('ICON_THEME',icon_theme) :
				self.ICON_THEME = icon_theme
				print ("Icon Theme Changed : " + self.ICON_THEME)
			else :
				self.ComboBox_icon.set_active_iter(get_iter(self.ComboBox_icon.get_model(),self.ICON_THEME))

	def cursor_theme_changed(self,e):
		cursor_theme = unicode(self.ComboBox_cursor.get_active_text(),'UTF_8')
		if unquote(self.CURSOR_THEME) != cursor_theme:
			if self.set_gdm('CURSOR_THEME',cursor_theme) :
				self.CURSOR_THEME = cursor_theme
				print ("Cursor Theme Changed : " + self.CURSOR_THEME)
			else :
				self.ComboBox_cursor.set_active_iter(get_iter(self.ComboBox_cursor.get_model(),self.CURSOR_THEME))

	def logo_icon_changed(self,e):
		logo_icon = unicode(self.Entry_logo_icon.get_text(),'UTF_8')
		if self.LOGO_ICON != logo_icon :
			if self.set_gdm('LOGO_ICON',logo_icon) :
				self.LOGO_ICON = logo_icon
				print ("Logo Icon Changed : " + self.LOGO_ICON)
			else:
				self.Entry_logo_icon.set_text(self.LOGO_ICON)

	def shell_logo_changed(self,e):
		shell_logo = self.BTN_shell_logo.get_filename()
		if self.SHELL_LOGO != shell_logo :
			if self.set_gdm('SHELL_LOGO',shell_logo) :
				self.SHELL_LOGO = shell_logo
				print ("Shell Logo Changed : " + self.SHELL_LOGO)
			else:
				self.BTN_shell_logo.set_filename(self.SHELL_LOGO)

	def banner_toggled(self,e):
		banner = self.CheckButton_banner.get_active()
		if banner!=self.BANNER :
			if self.set_gdm('BANNER',str(banner)) :
				self.BANNER = banner
				print ("Banner Changed : " + str(self.BANNER))
				if self.BANNER :
					self.Entry_banner_text.set_sensitive(True)
				else:
					self.Entry_banner_text.set_sensitive(False)
			else:
				self.CheckButton_banner.set_active(self.BANNER)

	def banner_text_changed(self,e):
		banner_text = unicode(self.Entry_banner_text.get_text(),'UTF_8')
		if banner_text!=self.BANNER_TEXT :
			if self.set_gdm('BANNER_TEXT',banner_text) :
				self.BANNER_TEXT = banner_text
				print ("Banner Text Changed : " + self.BANNER_TEXT)
			else :
				self.Entry_banner_text.set_text(self.BANNER_TEXT)

	def user_list_toggled(self,e):
		user_list = self.CheckButton_user.get_active()
		if self.USER_LIST != user_list :
			if self.set_gdm('USER_LIST',str(user_list).lower()) :
				self.USER_LIST = user_list
				print ("User List Changed : " + str(self.USER_LIST))
			else:
				self.CheckButton_user.set_active(self.USER_LIST)

	def menu_btn_toggled(self,e):
		menu_btn = self.CheckButton_restart.get_active()
		if self.MENU_BTN != menu_btn :
			if self.set_gdm('MENU_BTN',str(menu_btn)) :
				self.MENU_BTN = menu_btn
				print ("Menu Btn Changed : " + str(self.MENU_BTN))
			else:
				self.CheckButton_restart.set_active(self.MENU_BTN)

	def autologin_changed(self,e) :
		autologin_enabled = self.BTN_autologin.get_autologin()
		autologin_username = self.BTN_autologin.get_username()
		autologin_timed = self.BTN_autologin.get_timed()
		autologin_time = self.BTN_autologin.get_time()
		if self.set_autologin(autologin_enabled,autologin_username,autologin_timed,autologin_time) :
			print("Autologin Changed : " + autologin_username)
			self.AUTOLOGIN_ENABLED = autologin_enabled
			self.AUTOLOGIN_USERNAME = autologin_username
			self.AUTOLOGIN_TIMED = autologin_timed
			self.AUTOLOGIN_TIME = autologin_time
		else :
			self.BTN_autologin.set_autologin(self.AUTOLOGIN_ENABLED)
			self.BTN_autologin.set_username(self.AUTOLOGIN_USERNAME)
			self.BTN_autologin.set_timed(self.AUTOLOGIN_TIMED)
			self.BTN_autologin.set_time(self.AUTOLOGIN_TIME)

	def clock_date_toggled(self,e,state) :
		clock_date = self.Switch_clock_date.get_active()
		if self.CLOCK_DATE != clock_date :
			if self.set_gdm('CLOCK_DATE',str(clock_date).lower()) :
				self.CLOCK_DATE = clock_date
				print ("Clock Date toggled : " + str(self.CLOCK_DATE))
			else:
				self.Switch_clock_date.set_active(self.CLOCK_DATE)

	def clock_seconds_toggled(self,e,state) :
		clock_seconds = self.Switch_clock_seconds.get_active()
		if self.CLOCK_SECONDS != clock_seconds :
			if self.set_gdm('CLOCK_SECONDS',str(clock_seconds).lower()) :
				self.CLOCK_SECONDS = clock_seconds
				print ("Clock Seconds toggled : " + str(self.CLOCK_SECONDS))
			else:
				self.Switch_clock_seconds.set_active(self.CLOCK_SECONDS)

#-----------------------------------------------

def get_setting(name,data):
	for line in data:
		line = unicode(line)
		if -1 != line.find(name+"="):
			value = line[line.rfind("=")+1:len(line)].strip()
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

#-----------------------------------------------

MainWindow().show_all()

Gtk.main()

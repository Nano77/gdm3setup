#! /bin/sh
#
#

`dbus-launch | sed "s/^/export /"`
echo -n "GTK=" > /tmp/GET_GDM
gsettings get org.gnome.desktop.interface gtk-theme >> /tmp/GET_GDM
echo -n "ICON=" >> /tmp/GET_GDM
gsettings get org.gnome.desktop.interface icon-theme >> /tmp/GET_GDM
echo -n "CURSOR=" >> /tmp/GET_GDM
gsettings get org.gnome.desktop.interface cursor-theme >> /tmp/GET_GDM
echo -n "BKG=" >> /tmp/GET_GDM
gsettings get org.gnome.desktop.background picture-uri >> /tmp/GET_GDM
echo -n "LOGO=" >> /tmp/GET_GDM
gconftool-2 --get /apps/gdm/simple-greeter/logo_icon_name >> /tmp/GET_GDM
echo -n "USER_LIST=" >> /tmp/GET_GDM
gconftool-2 --get /apps/gdm/simple-greeter/disable_user_list >> /tmp/GET_GDM
echo -n "BTN=" >> /tmp/GET_GDM
gconftool-2 --get /apps/gdm/simple-greeter/disable_restart_buttons >> /tmp/GET_GDM
echo -n "BANNER=" >> /tmp/GET_GDM
gconftool-2 --get /apps/gdm/simple-greeter/banner_message_enable >> /tmp/GET_GDM
echo -n "BANNER_TEXT=" >> /tmp/GET_GDM
gconftool-2 --get /apps/gdm/simple-greeter/banner_message_text >> /tmp/GET_GDM



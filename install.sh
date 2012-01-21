#! /bin/sh
#
#

install --mode=755 -D gdm3setup.py /usr/bin/
install --mode=755 -D gdm3setup-daemon.py /usr/bin/
install --mode=755 -D start-gdm3setup-daemon /usr/bin/
install --mode=755 -D gdmlogin.py /usr/bin/
install --mode=755 -D get_gdm.sh /usr/bin/
install --mode=755 -D set_gdm.sh /usr/bin/
install -D gdm3setup.desktop /usr/share/applications/
install -D apps.nano77.gdm3setup.service /usr/share/dbus-1/system-services/
install -D apps.nano77.gdm3setup.service /usr/share/dbus-1/services/
install -D apps.nano77.gdm3setup.conf /etc/dbus-1/system.d/
install -D apps.nano77.gdm3setup.policy /usr/share/polkit-1/actions/
install -D gdm3setup.ui /usr/share/gdm3setup/ui/gdm3setup.ui
cp -r locale /usr/share/


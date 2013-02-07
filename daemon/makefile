all:
	sed -e 's/%PYTHON%/python2/;s/%GDM_BIN%/\/usr\/sbin\/gdm/;s/%GDM_CONF%/\/etc\/gdm\/custom.conf/;s/%GDM_USER%/gdm/' gdm3setup-daemon.in > gdm3setup-daemon
	sed -e 's/%PYTHON%/python2/;s/%GDM_CONF%/\/etc\/gdm\/custom.conf/' gdmlogin.in > gdmlogin
	sed -e 's/%GDM_BIN%/\/usr\/sbin\/gdm/' get_gdm.in > get_gdm
	sed -e 's/%PYTHON%/python2/' gdmshelltheme.in > gdmshelltheme

ubuntu:
	sed -e 's/%PYTHON%/python/;s/%GDM_BIN%/\/usr\/sbin\/gdm/;s/%GDM_CONF%/\/etc\/gdm\/custom.conf/;s/%GDM_USER%/gdm/' gdm3setup-daemon.in > gdm3setup-daemon
	sed -e 's/%PYTHON%/python/;s/%GDM_CONF%/\/etc\/gdm\/custom.conf/' gdmlogin.in > gdmlogin
	sed -e 's/%GDM_BIN%/\/usr\/sbin\/gdm/' get_gdm.in > get_gdm
	sed -e 's/%PYTHON%/python/' gdmshelltheme.in > gdmshelltheme

debian:
	sed -e 's/%PYTHON%/python/;s/%GDM_BIN%/\/usr\/sbin\/gdm3/;s/%GDM_CONF%/\/etc\/gdm3\/custom.conf/;s/%GDM_USER%/Debian-gdm/' gdm3setup-daemon.in > gdm3setup-daemon
	sed -e 's/%PYTHON%/python/;s/%GDM_CONF%/\/etc\/gdm3\/custom.conf/' gdmlogin.in > gdmlogin
	sed -e 's/%GDM_BIN%/\/usr\/sbin\/gdm3/' get_gdm.in > get_gdm
	sed -e 's/%PYTHON%/python/' gdmshelltheme.in > gdmshelltheme

clean:
	rm gdm3setup-daemon
	rm gdmlogin
	rm gdmshelltheme
	rm get_gdm

install:
	install --mode=755 -D gdm3setup-daemon $(DESTDIR)/usr/bin/gdm3setup-daemon
	install --mode=755 -D start-gdm3setup-daemon $(DESTDIR)/usr/bin/
	install --mode=755 -D gdmlogin $(DESTDIR)/usr/bin/
	install --mode=755 -D gdmshelltheme $(DESTDIR)/usr/bin/
	install --mode=755 -D get_gdm $(DESTDIR)/usr/bin/
	install --mode=755 -D set_gdm $(DESTDIR)/usr/bin/
	install -D apps.nano77.gdm3setup.service $(DESTDIR)/usr/share/dbus-1/system-services/apps.nano77.gdm3setup.service
	install -D apps.nano77.gdm3setup.service $(DESTDIR)/usr/share/dbus-1/services/apps.nano77.gdm3setup.service
	install -D apps.nano77.gdm3setup.conf $(DESTDIR)/etc/dbus-1/system.d/apps.nano77.gdm3setup.conf
	install -D apps.nano77.gdm3setup.policy $(DESTDIR)/usr/share/polkit-1/actions/apps.nano77.gdm3setup.policy

uninstall:
	rm $(DESTDIR)/usr/bin/gdm3setup-daemon
	rm $(DESTDIR)/usr/bin/start-gdm3setup-daemon
	rm $(DESTDIR)/usr/bin/gdmlogin
	rm $(DESTDIR)/usr/bin/gdmshelltheme
	rm $(DESTDIR)/usr/bin/get_gdm
	rm $(DESTDIR)/usr/bin/set_gdm
	rm $(DESTDIR)/usr/share/dbus-1/system-services/apps.nano77.gdm3setup.service 
	rm $(DESTDIR)/usr/share/dbus-1/services/apps.nano77.gdm3setup.service 
	rm $(DESTDIR)/etc/dbus-1/system.d/apps.nano77.gdm3setup.conf 
	rm $(DESTDIR)/usr/share/polkit-1/actions/apps.nano77.gdm3setup.policy 


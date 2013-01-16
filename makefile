
all: mo

ubuntu: python mo

debian: python mo
	sed -i -e 's/sbin\/gdm/sbin\/gdm3/' gdm3setup-daemon.py
	sed -i -e 's/sbin\/gdm/sbin\/gdm3/' gdm3setup.py
	sed -i -e 's/etc\/gdm/etc\/gdm3/' gdm3setup-daemon.py
	sed -i -e 's/etc\/gdm/etc\/gdm3/' gdmlogin.py
	sed -i -e 's/"gdm"/"Debian-gdm"/' gdm3setup-daemon.py
	sed -i -e 's/sbin\/gdm/sbin\/gdm3/' get_gdm.sh

python:
	sed -i s/python2/python/ gdm3setup.py
	sed -i s/python2/python/ gdm3setup-daemon.py
	sed -i s/python2/python/ gdmlogin.py

mo:
	mkdir -p locale/{fr,en_US,es_ES,de_DE,it,pt_BR,zh_CN}/LC_MESSAGES/

	msgfmt po/gdm3setup-fr.po -o locale/fr/LC_MESSAGES/gdm3setup.mo
	msgfmt po/gdm3setup-en_US.po -o locale/en_US/LC_MESSAGES/gdm3setup.mo
	msgfmt po/gdm3setup-es_ES.po -o locale/es_ES/LC_MESSAGES/gdm3setup.mo
	msgfmt po/gdm3setup-de_DE.po -o locale/de_DE/LC_MESSAGES/gdm3setup.mo
	msgfmt po/gdm3setup-it.po -o locale/it/LC_MESSAGES/gdm3setup.mo
	msgfmt po/gdm3setup-pt_BR.po -o locale/pt_BR/LC_MESSAGES/gdm3setup.mo
	msgfmt po/gdm3setup-zh_CN.po -o locale/zh_CN/LC_MESSAGES/gdm3setup.mo

install:
	install --mode=755 -D gdm3setup.py $(DESTDIR)/usr/bin/gdm3setup.py
	install --mode=755 -D gdm3setup-daemon.py $(DESTDIR)/usr/bin/gdm3setup-daemon.py
	install --mode=755 -D start-gdm3setup-daemon $(DESTDIR)/usr/bin/
	install --mode=755 -D gdmlogin.py $(DESTDIR)/usr/bin/
	install --mode=755 -D get_gdm.sh $(DESTDIR)/usr/bin/
	install --mode=755 -D set_gdm.sh $(DESTDIR)/usr/bin/
	install -D gdm3setup.desktop $(DESTDIR)/usr/share/applications/gdm3setup.desktop
	install -D apps.nano77.gdm3setup.service $(DESTDIR)/usr/share/dbus-1/system-services/apps.nano77.gdm3setup.service
	install -D apps.nano77.gdm3setup.service $(DESTDIR)/usr/share/dbus-1/services/apps.nano77.gdm3setup.service
	install -D apps.nano77.gdm3setup.conf $(DESTDIR)/etc/dbus-1/system.d/apps.nano77.gdm3setup.conf
	install -D apps.nano77.gdm3setup.policy $(DESTDIR)/usr/share/polkit-1/actions/apps.nano77.gdm3setup.policy
	install -D gdm3setup.ui $(DESTDIR)/usr/share/gdm3setup/ui/gdm3setup.ui
	cp -r locale $(DESTDIR)/usr/share/

uninstall:
	rm /usr/bin/gdm3setup.py
	rm /usr/bin/gdm3setup-daemon.py
	rm /usr/bin/start-gdm3setup-daemon
	rm /usr/bin/gdmlogin.py
	rm /usr/bin/get_gdm.sh
	rm /usr/bin/set_gdm.sh
	rm /usr/share/applications/gdm3setup.desktop 
	rm /usr/share/dbus-1/system-services/apps.nano77.gdm3setup.service 
	rm /usr/share/dbus-1/services/apps.nano77.gdm3setup.service 
	rm /etc/dbus-1/system.d/apps.nano77.gdm3setup.conf 
	rm /usr/share/polkit-1/actions/apps.nano77.gdm3setup.policy 
	rm /usr/share/gdm3setup/ui/gdm3setup.ui
	rm /usr/share/locale/{de_DE,en_US,es_ES,fr,it,pt_BR,zh_CN}/LC_MESSAGES/gdm3setup.mo




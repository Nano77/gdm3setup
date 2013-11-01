all: mo
	sed -e 's/%PYTHON%/python2/;s/%GDM_BIN%/\/usr\/sbin\/gdm/' gdm3setup.in > gdm3setup

ubuntu: mo
	sed -e 's/%PYTHON%/python/;s/%GDM_BIN%/\/usr\/sbin\/gdm/' gdm3setup.in > gdm3setup

debian: mo
	sed -e 's/%PYTHON%/python/;s/%GDM_BIN%/\/usr\/sbin\/gdm3/' gdm3setup.in > gdm3setup

mo:
	$(MAKE) -C po

clean:
	rm gdm3setup
	$(MAKE) -C po clean

install:
	install --mode=755 -D gdm3setup $(DESTDIR)/usr/bin/gdm3setup
	install -D gdm3setup.desktop $(DESTDIR)/usr/share/applications/gdm3setup.desktop
	install -D gdm3setup.ui $(DESTDIR)/usr/share/gdm3setup/ui/gdm3setup.ui
	install -D dev/app-menu.ui $(DESTDIR)/usr/share/gdm3setup/ui/app-menu.ui
	$(MAKE) -C po install

uninstall:
	rm $(DESTDIR)/usr/bin/gdm3setup
	rm $(DESTDIR)/usr/share/applications/gdm3setup.desktop 
	rm $(DESTDIR)/usr/share/gdm3setup/ui/gdm3setup.ui
	rm $(DESTDIR)/usr/share/gdm3setup/ui/app-menu.ui
	$(MAKE) -C po uninstall




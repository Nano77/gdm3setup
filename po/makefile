
all:
	mkdir -p locale/{fr,en_US,es_ES,de_DE,it,pt_BR,zh_CN}/LC_MESSAGES/

	msgfmt gdm3setup-fr.po -o locale/fr/LC_MESSAGES/gdm3setup.mo
	msgfmt gdm3setup-en_US.po -o locale/en_US/LC_MESSAGES/gdm3setup.mo
	msgfmt gdm3setup-es_ES.po -o locale/es_ES/LC_MESSAGES/gdm3setup.mo
	msgfmt gdm3setup-de_DE.po -o locale/de_DE/LC_MESSAGES/gdm3setup.mo
	msgfmt gdm3setup-it.po -o locale/it/LC_MESSAGES/gdm3setup.mo
	msgfmt gdm3setup-pt_BR.po -o locale/pt_BR/LC_MESSAGES/gdm3setup.mo
	msgfmt gdm3setup-zh_CN.po -o locale/zh_CN/LC_MESSAGES/gdm3setup.mo

clean:
	rm -r locale

install:
	cp -r locale $(DESTDIR)/usr/share/

uninstall:
	rm $(DESTDIR)/usr/share/locale/{de_DE,en_US,es_ES,fr,it,pt_BR,zh_CN}/LC_MESSAGES/gdm3setup.mo




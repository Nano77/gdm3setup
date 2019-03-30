
LOCALES := $(shell tail -n +2 LINGUAS )

all:
	intltool-update --pot -g gdm3setup
	intltool-update -r -g gdm3setup

	@for locale in $(LOCALES); do \
        	mkdir -p locale/$$locale/LC_MESSAGES/; \
        	msgfmt gdm3setup-$$locale.po -o locale/$$locale/LC_MESSAGES/gdm3setup.mo; \
	done

clean:
	rm -r locale

install:
	cp -r locale $(DESTDIR)/usr/share/

uninstall:
	@for locale in $(LOCALES); do \
        	rm $(DESTDIR)/usr/share/locale/$$locale/LC_MESSAGES/gdm3setup.mo; \
	done





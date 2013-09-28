
all:
	$(MAKE) -C gui
	$(MAKE) -C utils

ubuntu: 
	$(MAKE) -C gui ubuntu
	$(MAKE) -C utils ubuntu

debian: 
	$(MAKE) -C gui debian
	$(MAKE) -C utils debian

clean:
	$(MAKE) -C gui clean
	$(MAKE) -C utils clean

install:
	$(MAKE) -C gui install
	$(MAKE) -C utils install

uninstall:
	$(MAKE) -C gui uninstall
	$(MAKE) -C utils uninstall


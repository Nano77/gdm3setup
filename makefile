
all:
	$(MAKE) -C src
	$(MAKE) -C daemon

ubuntu: 
	$(MAKE) -C src ubuntu
	$(MAKE) -C daemon ubuntu

debian: 
	$(MAKE) -C src debian
	$(MAKE) -C daemon debian

clean:
	$(MAKE) -C src clean
	$(MAKE) -C daemon clean

install:
	$(MAKE) -C src install
	$(MAKE) -C daemon install

uninstall:
	$(MAKE) -C src uninstall
	$(MAKE) -C daemon uninstall


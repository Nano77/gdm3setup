Build
-----

Standard :  `make`



Ubuntu : `make ubuntu`



Debian : `make debian`




Install
-------

`make DESTDIR=`*'Your desired destination'* `install`




Ubuntu post-install
-------------------

Ensure than `/var/lib/gdm/dconf` are writable by gdm :  
`chown -R gdm:gdm /var/lib/gdm/`



#! /bin/sh
#
#

`dbus-launch | sed "s/^/export /"`

set_gdm.py $*


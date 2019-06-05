# Generating up-to-date PO files for translation

## 1. Generate an up-to-date POT template

To create an up-to-date PO template file (.pot) from the current source:

$ intltool-update --pot -g gdm3setup

## 2. Update all PO files with latest translatable strings

$ intltool-update -r -g gdm3setup

It uses the template file for referene. Existing translations are kept, of course.

# Adding a new language

Insert the language code into the LINGUAS file and update the PO files as described above.

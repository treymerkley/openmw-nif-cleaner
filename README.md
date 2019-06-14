# OpenMW NIF Cleaner
OpenMW NIF Cleaner edits mods made for the original engine to remove the shiny texture problem and re-implement *most* normal maps by fixing their naming convention.

## Install
ONC depends on:

+ Python 3.7
+ Pyffi version 2.2.2. Note that higher versions are incompatible with NIF files used for Morrowind, but 2.2.2 is perfectly stable. If you need newer versions of Pyffi for editing meshes in new Bethesda games, you should be able to set this up in a venv.
+ (Optional) PyQt5 >=5.12.2

Once you have these installed, simply clone the files and run either the console version or the Qt version for a GUI.
